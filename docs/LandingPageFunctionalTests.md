# Landing Page Functional Development Tests

## Scope

These tests cover only Tiffany Davidson's assigned Moffat Bay landing page (`index.html`) and its landing page backend endpoint.

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

The default configuration uses `localhost`, port `3306`, user `root`, database `moffat_bay`, and a blank password.

## FT-LP-01: Landing Page Loads With Production Navigation

Purpose: Verify that the landing page loads successfully and contains the required production navigation and JavaScript without references to the removed mock application files.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Run:

```text
python -m pytest src/api/tests/test_landing_api.py::test_landing_page_loads_with_production_navigation_and_script -v
```

Expected Result: The test displays `PASSED`. The landing page returns HTTP 200, includes the Book and Rooms links, includes `landing.js`, and does not reference the removed `mock-data.js`, `api-contract.js`, or `app.js` files.

Actual Result: ______________________________

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-LP-02: Landing API Returns Room Data From MySQL

Purpose: Verify that the landing page backend connects to the shared `moffat_bay` database and returns the four room types and nightly prices from `RoomTypes`.

Steps:

1. Make sure MySQL is running and the schema/seed scripts have already been loaded.
2. From the project folder, run:

```text
python -m pytest src/api/tests/test_landing_api.py::test_landing_room_api_returns_seeded_room_types_from_database -v
```

Expected Result: The test displays `PASSED`. The API returns HTTP 200 and the four seeded room types: Double Full Beds, Queen, Double Queen Beds, and King, with prices of $120, $135, $150, and $160 per night.

Actual Result: ______________________________

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## Run Both Tests Together

```text
python -m pytest src/api/tests/test_landing_api.py -v
```

A successful run should finish with `2 passed`.

## Browser Verification for the Finished Landing Page

Run the landing server:

```text
python src/api/landing_api.py
```

Then open:

```text
http://127.0.0.1:8000/
```

The room cards should be populated from the database. You can also open the API directly at:

```text
http://127.0.0.1:8000/api/landing/room-types
```

The API page should display JSON containing the four room types. This is useful as additional screenshot evidence that the frontend is connected to the Python/MySQL backend.
