# Login Page Functional Development Tests

## Scope

These tests cover only Brayan Cova's assigned Moffat Bay login page (`login.html`) and its login API endpoint.

## Preconditions

1. MySQL is running.
2. `src/sql/schema.sql` has been executed.
3. `src/sql/seed.sql` has been executed (seeds the demo account used below).
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

## FT-LOGIN-01: Login Page Loads With Production Scripts

Purpose: Verify that the login page loads successfully and references only its production scripts, with no leftover references to the removed mock application files.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Run:

```text
python -m pytest src/api/tests/test_login_api.py::test_login_page_loads_with_production_scripts_and_no_removed_files -v
```

Expected Result: The test displays `PASSED`. The login page returns HTTP 200, includes `emailValidation.js`, `auth-chip.js`, and `login.js`, and does not reference the removed `mock-data.js`, `api-contract.js`, or `app.js` files.

Actual Result: **************\_\_**************

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-LOGIN-02: Login API Accepts The Seeded Demo Account

Purpose: Verify that the login API connects to the shared `moffat_bay` database and authenticates the seeded demo customer.

Steps:

1. Make sure MySQL is running and the schema/seed scripts have already been loaded.
2. From the project folder, run:

```text
python -m pytest src/api/tests/test_login_api.py::test_login_api_returns_success_for_seeded_demo_account -v
```

Expected Result: The test displays `PASSED`. Posting `demo@moffatbay.com` / `DemoPass1` to `/api/auth/login` returns HTTP 200 with `success: true`, `first_name: "Demo"`, and a numeric `customer_id`.

Actual Result: **************\_\_**************

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-LOGIN-03: Login API Rejects An Incorrect Password With A Generic Message

Purpose: Verify that an incorrect password is rejected without revealing whether the email itself is registered (avoids user enumeration).

Steps:

1. Make sure MySQL is running and the schema/seed scripts have already been loaded.
2. From the project folder, run:

```text
python -m pytest src/api/tests/test_login_api.py::test_login_api_returns_generic_error_for_invalid_password -v
```

Expected Result: The test displays `PASSED`. Posting `demo@moffatbay.com` with the wrong password to `/api/auth/login` returns HTTP 401 with `success: false` and the reason `"Invalid email or password."`.

Actual Result: **************\_\_**************

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## Run All Three Tests Together

```text
python -m pytest src/api/tests/test_login_api.py -v
```

A successful run should finish with `3 passed`.

## Browser Verification for the Finished Login Page

Run the login server (separate from the landing server, on its own port):

```text
python src/api/login_api.py
```

Then open:

```text
http://127.0.0.1:8001/login.html
```

Log in with the demo account (`demo@moffatbay.com` / `DemoPass1`). On success you should be redirected to `reservation.html`, and the header's account area should switch from Login/Register links to a "Welcome, Demo" greeting with a Logout button. This is useful as additional screenshot evidence that the frontend is connected to the Python/MySQL backend.
