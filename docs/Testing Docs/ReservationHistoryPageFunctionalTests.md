# Reservation History Page Functional Development Tests

## Scope

These tests cover only the reservation history lookup from the Reservation Lookup page (`reservation-lookup.html`).

## Preconditions

1. MySQL is running.
2. `src/sql/schema.sql` has been executed.
3. `src/sql/seed.sql` has been executed (seeds demo customer and reservation history used below).
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

## FT-RH-01: History Requires a Customer ID

Objective: Verify that `GET /api/reservations/history` rejects a request that is missing the `customer_id` query parameter, so reservation history can never be requested without identifying a customer.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_history_api.py::test_history_requires_customer_id -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Requesting `/api/reservations/history` with no `customer_id` query parameter returns HTTP 400 with an `error` field in the response body.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-RH-02: History Returns the Seeded Reservation With Line Items

Objective: Verify that `GET /api/reservations/history` returns the seeded demo customer's past reservation along with its room line items, so a returning guest can see their booking details.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded, so the seeded customer (`customer_id: 1`) and their reservation exist.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_history_api.py::test_history_returns_seeded_reservation_with_line_items -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Requesting `/api/reservations/history?customer_id=1` returns HTTP 200 with at least one reservation entry that has a `check_in_date`, `check_out_date`, a `total_price` greater than `0`, and at least one `line_items` entry with a `room_number`.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-RH-03: History Returns an Empty List for an Unknown Customer

Objective: Verify that `GET /api/reservations/history` returns an empty list rather than an error for a `customer_id` with no reservations, so the lookup page can show a "no history" state instead of failing.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Confirm MySQL is running and that `schema.sql`/`seed.sql` have already been loaded.
3. Set `MOFFAT_DB_PASSWORD` (or the other `MOFFAT_DB_*` variables) if your local database needs non-default connection settings.
4. Confirm `pytest` and `mysql-connector-python` are installed (see Preconditions).
5. Run the targeted test:

```text
python -m pytest src/api/tests/test_reservation_history_api.py::test_history_returns_empty_list_for_unknown_customer -v
```

6. Review the terminal output to confirm the test result and the returned status code/response body logged by the test.

Expected Result: The test displays `PASSED`. Requesting `/api/reservations/history?customer_id=999999` (a customer id that does not exist) returns HTTP 200 with `reservations: []`.

Actual Result: ******\*\*******\_\_******\*\*******

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## Run All Three Tests Together

```text
python -m pytest src/api/tests/test_reservation_history_api.py -v
```

A successful run should finish with `3 passed`.

## Browser Verification for the Finished Reservation History Flow

Run the shared dev server:

```text
python src/api/startup_api.py
```

Then open:

```text
http://127.0.0.1:8000/reservation-lookup.html
```

Log in with the demo account and confirm the page lists the seeded reservation with its room line items. This is useful as additional screenshot evidence that the frontend is connected to the reservation history API.
