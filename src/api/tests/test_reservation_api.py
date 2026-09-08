"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Functional development tests for the reservation availability and creation
API endpoints, using the actual local MySQL database (seeded via
sql/seed.sql).
"""

import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from api.startup_api import create_server


def _start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_test_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def _post(base_url, path, payload):
    request = Request(
        f"{base_url}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def test_availability_rejects_invalid_date_range():
    """FT-RES-01: check-out on or before check-in should be rejected."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post(
            base_url,
            "/api/reservations/availability",
            {"check_in": "2026-09-20", "check_out": "2026-09-20", "rooms": [{"room_type_id": 1, "quantity": 1}]},
        )

        assert status == 200
        assert payload["ok"] is False
    finally:
        _stop_test_server(server, thread)


def test_availability_reports_free_rooms_for_open_dates():
    """FT-RES-02: a far-future date range with no seeded bookings should be available."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post(
            base_url,
            "/api/reservations/availability",
            {"check_in": "2027-01-10", "check_out": "2027-01-12", "rooms": [{"room_type_id": 1, "quantity": 1}]},
        )

        assert status == 200
        assert payload["ok"] is True
        assert payload["details"][0]["available_count"] >= 1
    finally:
        _stop_test_server(server, thread)


def test_create_reservation_requires_customer_id():
    """FT-RES-03: a missing customer_id should be rejected without touching the database."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post(
            base_url,
            "/api/reservations",
            {
                "guests": 2,
                "check_in": "2027-02-01",
                "check_out": "2027-02-03",
                "rooms": [{"room_type_id": 1, "quantity": 1}],
            },
        )

        assert status == 400
        assert payload["success"] is False
    finally:
        _stop_test_server(server, thread)


def test_create_reservation_succeeds_for_open_dates():
    """FT-RES-04: a valid booking on open dates should create a reservation."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post(
            base_url,
            "/api/reservations",
            {
                "customer_id": 1,
                "guests": 2,
                "check_in": "2027-03-01",
                "check_out": "2027-03-03",
                "rooms": [{"room_type_id": 2, "quantity": 1}],
            },
        )

        assert status == 200
        assert payload["success"] is True
        assert isinstance(payload["reservation_id"], int)
        assert float(payload["total_price"]) > 0
    finally:
        _stop_test_server(server, thread)
