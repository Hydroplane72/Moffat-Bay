"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Two functional development tests for the Moffat Bay about page.

Test 1 verifies that the production about page is served with the merged
contact section, its inquiry form, and the about.js script.

Test 2 verifies that the contact API can insert a new inquiry into the real
local MySQL ContactMessages table and returns the new row's id.
"""

import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from api.about_api import create_server


def _start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_test_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def _post_contact_message(base_url, name, email, subject, message):
    request = Request(
        f"{base_url}/api/contact",
        data=json.dumps(
            {"name": name, "email": email, "subject": subject, "message": message}
        ).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def test_about_page_loads_with_contact_section_and_script():
    """FT-AB-01: The about page should load with its merged contact section."""
    server, thread = _start_test_server()

    try:
        url = f"http://127.0.0.1:{server.server_port}/about.html"

        with urlopen(url, timeout=5) as response:
            html = response.read().decode("utf-8")
            status = response.status

        assert status == 200
        assert 'id="contact"' in html
        assert 'id="contact-form"' in html
        assert 'src="assets/js/about.js"' in html
        assert 'href="contact.html"' not in html
        assert "mock-data.js" not in html
        assert "api-contract.js" not in html
        assert "app.js" not in html
    finally:
        _stop_test_server(server, thread)


def test_contact_api_inserts_new_message_into_database():
    """FT-AB-02: The contact API should insert a new row into ContactMessages."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post_contact_message(
            base_url,
            "Functional Test",
            "functional.test@example.com",
            "Automated Test Inquiry",
            "This message was submitted by an automated functional test.",
        )

        assert status == 200
        assert payload["success"] is True
        assert isinstance(payload["message_id"], int)
    finally:
        _stop_test_server(server, thread)
