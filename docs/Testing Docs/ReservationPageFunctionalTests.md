# Reservation Page Functional Development Tests

## Scope

These tests cover only the reservation booking from the Reservation page (`reservation.html`) and Reservation Summary page (`reservation-summary.html`).

Rashai Robertson's assigned portion is reservation **availability** (FT-RES-01 and FT-RES-02)

Brayan Covarrubias's assigned portion is reservation **creation** (FT-RES-03 and FT-RES-04).

## Preconditions

1. MySQL is running.
2. `src/sql/schema.sql` has been executed.
3. `src/sql/seed.sql` has been executed.
4. Python 3.9 or newer is installed.
5. Install the required packages if needed:

```text
python -m pip install pytest mysql-connector-python
```

If the local MySQL `root` account has a password, set it before running the server or tests:

Windows Command Prompt:

```text
set MOFFAT_DB_PASSWORD=your_password_here
```

PowerShell:

```text
$env:MOFFAT_DB_PASSWORD="your_password_here"
```

macOS/Linux:

```text
export MOFFAT_DB_PASSWORD=your_password_here
```

The default configuration uses `localhost`, port `3306`, user `root`, database `moffat_bay`, and a blank password.

## FT-RES-01: Availability Rejects an Invalid Date Range

Objective: Verify that `POST /api/reservations/availability` rejects a request where the check-out date is on or before the check-in date, so a stay with zero or negative nights can never be checked as available.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_api.py::test_availability_rejects_invalid_date_range -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Posting a payload with `check_in` and `check_out` set to the same date (`2026-09-20`) to `/api/reservations/availability` returns HTTP 200 with `ok: false`.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-RES-02: Availability Reports Free Rooms For Open Dates

Objective: Verify that `POST /api/reservations/availability` reports available rooms for a far-future date range with no seeded bookings, so a guest can confirm a room type is bookable before adding it to their cart.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded, so the seeded room types and rooms exist.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_api.py::test_availability_reports_free_rooms_for_open_dates -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Posting a payload requesting one `room_type_id: 1` room for `check_in: 2027-01-10` to `check_out: 2027-01-12` (a far-future range with no seeded bookings) to `/api/reservations/availability` returns HTTP 200 with `ok: true` and a `details[0].available_count` of at least `1`.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-RES-03: Reservation Creation Requires a Customer ID

Objective: Verify that `POST /api/reservations` rejects a reservation request that is missing `customer_id`, without creating any row in the `Reservations` table, so a booking can never be created without a customer attached to it.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_api.py::test_create_reservation_requires_customer_id -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Posting a reservation payload with `guests`, `check_in`, `check_out`, and `rooms` but **no** `customer_id` to `/api/reservations` returns HTTP 400 with `success: false` and a reason indicating a logged-in customer is required. No reservation row is inserted.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-RES-04: Reservation Creation Succeeds For Open Dates

Objective: Verify that a complete, valid reservation request (existing `customer_id`, valid guest count, an open future date range, and an available room type) is accepted end-to-end: availability is confirmed, a `Reservations` row and its linked `ReservationRooms` row are created, and the API returns a confirmation number with a positive total price.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded, so the seeded customer (`customer_id: 1`) and room types exist.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_api.py::test_create_reservation_succeeds_for_open_dates -v
```

6. Review the terminal output to confirm the test result, then optionally query the `Reservations` and `ReservationRooms` tables for the far-future date used in the test (`2027-03-01` to `2027-03-03`) to confirm the new rows were persisted.

Expected Result: The test displays `PASSED`. Posting a valid reservation payload (`customer_id: 1`, `guests: 2`, `check_in: 2027-03-01`, `check_out: 2027-03-03`, one `Queen` room) to `/api/reservations` returns HTTP 200 with `success: true`, a numeric `reservation_id`, and a `total_price` greater than `0`.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## Run All Four Tests Together

```text
python -m pytest src/api/tests/test_reservation_api.py -v
```

A successful run should finish with `4 passed`.

## Browser Verification for the Finished Reservation Creation Flow

Run the shared dev server:

```text
python src/api/startup_api.py
```

Then open:

```text
http://127.0.0.1:8000/reservation.html
```

Log in with the demo account, add a room to the cart with a future check-in/check-out range, continue to the Reservation Summary page, and confirm the booking. On success you should see a confirmation message with a reservation number. This is useful as additional screenshot evidence that the frontend is connected to the reservation creation API.
