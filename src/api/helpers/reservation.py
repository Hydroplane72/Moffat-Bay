"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Reservation availability checking (via the get_room_availability stored
procedure) and reservation creation, kept separate from the HTTP server so
the logic can be unit tested on its own.
"""

from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Dict, List

from api.models.availability_result import AvailabilityResult, RoomTypeAvailability
from api.models.reservation_result import ReservationResult

DATE_FORMAT = "%Y-%m-%d"


def _parse_date(value) -> date:
    if isinstance(value, date):
        return value
    return datetime.strptime(str(value), DATE_FORMAT).date()


def _normalize_room_requests(room_requests) -> Dict[int, int]:
    """Merge duplicate room_type_id entries into a single quantity each."""
    merged: Dict[int, int] = {}

    for entry in room_requests:
        room_type_id = int(entry["room_type_id"])
        quantity = int(entry["quantity"])
        merged[room_type_id] = merged.get(room_type_id, 0) + quantity

    return merged


def _fetch_room_type_prices(connection, room_type_ids) -> Dict[int, Decimal]:
    if not room_type_ids:
        return {}

    placeholders = ", ".join(["%s"] * len(room_type_ids))
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            f"SELECT room_type_id, price_per_night FROM RoomTypes WHERE room_type_id IN ({placeholders})",
            tuple(room_type_ids),
        )
        rows = cursor.fetchall()
    finally:
        cursor.close()

    return {int(row["room_type_id"]): Decimal(str(row["price_per_night"])) for row in rows}


def _fetch_room_type_map(connection) -> Dict[int, int]:
    """Map room_id -> room_type_id for every room in the lodge."""
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT room_id, room_type_id FROM Rooms")
        rows = cursor.fetchall()
    finally:
        cursor.close()

    return {int(row["room_id"]): int(row["room_type_id"]) for row in rows}


def _fetch_available_room_ids(connection, check_in: date, last_night: date, room_id_to_type: Dict[int, int]) -> Dict[int, List[int]]:
    """Run get_room_availability and return room ids that are free for every occupied night, grouped by room_type_id."""
    cursor = connection.cursor()

    try:
        cursor.callproc("get_room_availability", (check_in, last_night))

        statuses: Dict[int, set] = {}
        for result in cursor.stored_results():
            for row in result.fetchall():
                # Row shape: calendar_date, room_id, room_number, room_type_name, allow_reservations, availability_status
                room_id = int(row[1])
                status = str(row[5])
                statuses.setdefault(room_id, set()).add(status)
    finally:
        cursor.close()

    available_by_type: Dict[int, List[int]] = {}

    for room_id, seen_statuses in statuses.items():
        if seen_statuses == {"Available"}:
            room_type_id = room_id_to_type.get(room_id)
            if room_type_id is not None:
                available_by_type.setdefault(room_type_id, []).append(room_id)

    return available_by_type


def check_room_availability(connection, check_in, check_out, room_requests) -> AvailabilityResult:
    """Check whether the requested room types/quantities are free for every
    night of the stay (check_in inclusive, check_out exclusive)."""
    if not room_requests:
        return AvailabilityResult(ok=False, reason="At least one room is required.")

    try:
        check_in_date = _parse_date(check_in)
        check_out_date = _parse_date(check_out)
    except (ValueError, TypeError):
        return AvailabilityResult(ok=False, reason="Check-in and check-out dates must be valid dates.")

    if check_out_date <= check_in_date:
        return AvailabilityResult(ok=False, reason="Check-out date must be after check-in date.")

    try:
        requested_by_type = _normalize_room_requests(room_requests)
    except (KeyError, TypeError, ValueError):
        return AvailabilityResult(ok=False, reason="Each room must include a room_type_id and a positive quantity.")

    if any(quantity <= 0 for quantity in requested_by_type.values()):
        return AvailabilityResult(ok=False, reason="Room quantities must be greater than zero.")

    known_prices = _fetch_room_type_prices(connection, list(requested_by_type.keys()))
    unknown_types = [t for t in requested_by_type if t not in known_prices]
    if unknown_types:
        return AvailabilityResult(ok=False, reason="One or more selected room types no longer exist.")

    room_id_to_type = _fetch_room_type_map(connection)
    last_night = check_out_date - timedelta(days=1)
    available_by_type = _fetch_available_room_ids(connection, check_in_date, last_night, room_id_to_type)

    details = []
    overall_ok = True

    for room_type_id, requested in requested_by_type.items():
        available_room_ids = available_by_type.get(room_type_id, [])
        line_ok = len(available_room_ids) >= requested
        overall_ok = overall_ok and line_ok
        details.append(
            RoomTypeAvailability(
                room_type_id=room_type_id,
                requested=requested,
                available_count=len(available_room_ids),
                ok=line_ok,
            )
        )

    reason = "All requested rooms are available." if overall_ok else "Not enough rooms are available for one or more selected room types."

    return AvailabilityResult(
        ok=overall_ok,
        reason=reason,
        details=details,
        assigned_room_ids=available_by_type if overall_ok else None,
    )


def create_reservation(connection, customer_id, guests, check_in, check_out, room_requests) -> ReservationResult:
    """Re-validate availability and create the reservation and its rooms in one transaction."""
    if not customer_id:
        return ReservationResult(success=False, reason="A logged-in customer is required.")

    try:
        guests = int(guests)
    except (TypeError, ValueError):
        return ReservationResult(success=False, reason="Number of guests is required.")

    if guests <= 0:
        return ReservationResult(success=False, reason="Number of guests must be greater than zero.")

    availability = check_room_availability(connection, check_in, check_out, room_requests)
    if not availability.ok:
        return ReservationResult(success=False, reason=availability.reason)

    check_in_date = _parse_date(check_in)
    check_out_date = _parse_date(check_out)
    nights = (check_out_date - check_in_date).days

    requested_by_type = _normalize_room_requests(room_requests)
    prices = _fetch_room_type_prices(connection, list(requested_by_type.keys()))
    total_price = sum(prices[t] * nights * qty for t, qty in requested_by_type.items())

    try:
        # mysql-connector connections default to autocommit=False, so the
        # earlier availability check already left an implicit transaction
        # open; committing/rolling back below is enough without start_transaction().
        cursor = connection.cursor()

        try:
            cursor.execute(
                """
                INSERT INTO Reservations
                    (customer_id, num_guests, check_in_date, check_out_date, total_price, reservation_status)
                VALUES (%s, %s, %s, %s, %s, 'confirmed')
                """,
                (customer_id, guests, check_in_date, check_out_date, total_price),
            )
            reservation_id = cursor.lastrowid

            for room_type_id, quantity in requested_by_type.items():
                room_ids = availability.assigned_room_ids[room_type_id][:quantity]
                nightly_rate = prices[room_type_id]

                for room_id in room_ids:
                    cursor.execute(
                        """
                        INSERT INTO ReservationRooms (reservation_id, room_id, nightly_rate)
                        VALUES (%s, %s, %s)
                        """,
                        (reservation_id, room_id, nightly_rate),
                    )

            connection.commit()
        finally:
            cursor.close()
    except Exception:
        connection.rollback()
        return ReservationResult(success=False, reason="Unable to create the reservation at this time.")

    return ReservationResult(
        success=True,
        reason="Reservation confirmed.",
        reservation_id=int(reservation_id),
        total_price=f"{total_price:.2f}",
    )
