# About Page Functional Development Tests

## Scope

These tests cover only Brayan Cova's assigned Moffat Bay about page (`about.html`), which now
includes the merged "Contact Moffat Bay Lodge" section and its inquiry form.

## Preconditions

1. MySQL is running.
2. `src/sql/schema.sql` has been executed (creates the `ContactMessages` table).
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

## FT-AB-01: About Page Loads With Merged Contact Section

Purpose: Verify that the about page loads successfully, contains the merged
contact section and inquiry form, references its production `about.js`
script, and no longer links to the removed `contact.html` page.

Steps:

1. Open a terminal in the Moffat-Bay project folder.
2. Run:

```text
python -m pytest src/api/tests/test_about_api.py::test_about_page_loads_with_contact_section_and_script -v
```

Expected Result: The test displays `PASSED`. The about page returns HTTP 200,
includes `id="contact"` and `id="contact-form"`, includes `assets/js/about.js`,
and does not reference `contact.html`, `mock-data.js`, `api-contract.js`, or
`app.js`.

Actual Result: **************\_\_**************

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## FT-AB-02: Contact API Inserts A New Message Into The Database

Purpose: Verify that the about page's contact API connects to the shared
`moffat_bay` database and inserts a new inquiry into `ContactMessages`.

Steps:

1. Make sure MySQL is running and the schema/seed scripts have already been loaded.
2. From the project folder, run:

```text
python -m pytest src/api/tests/test_about_api.py::test_contact_api_inserts_new_message_into_database -v
```

Expected Result: The test displays `PASSED`. Posting a name, email, subject,
and message to `/api/contact` returns HTTP 200 with `success: true` and a
numeric `message_id`.

Actual Result: **************\_\_**************

Screenshot Evidence: Capture the terminal showing the test name and `PASSED`.

## Run Both Tests Together

```text
python -m pytest src/api/tests/test_about_api.py -v
```

A successful run should finish with `2 passed`.

## Browser Verification for the Finished About Page

Run the about page server (separate from the other feature servers, on its own port):

```text
python src/api/about_api.py
```

Then open:

```text
http://127.0.0.1:8004/about.html
```

Scroll to the "Contact Moffat Bay Lodge" section and submit the "Send an
Inquiry" form. On success the form should show "Thanks! Your message has
been sent." Confirm the row was saved by running the `ContactMessages` query
in `src/sql/view_tables.sql` against the `moffat_bay` database. This is
useful as additional screenshot evidence that the frontend is connected to
the Python/MySQL backend.
