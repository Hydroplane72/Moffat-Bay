"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Functional development tests for the login page and its login API endpoint.

Test 1 verifies that the login page is served with the production login
scripts and no references to the removed mock application files.

Test 2 and 3 verify that the login API accepts the seeded demo account and
rejects an incorrect password with a generic message, using the actual local
MySQL database.
"""

import json
import threading
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from api.login_api import create_server


def _start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_test_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def _post_login(base_url, email, password):
    request = Request(
        f"{base_url}/api/auth/login",
        data=json.dumps({"email": email, "password": password}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def test_login_page_loads_with_production_scripts_and_no_removed_files():
    """FT-LOGIN-01: The login page should load with its production scripts."""
    server, thread = _start_test_server()

    try:
        url = f"http://127.0.0.1:{server.server_port}/login.html"

        with urlopen(url, timeout=5) as response:
            html = response.read().decode("utf-8")
            status = response.status

        assert status == 200
        assert 'src="assets/js/emailValidation.js"' in html
        assert 'src="assets/js/auth-chip.js"' in html
        assert 'src="assets/js/login.js"' in html
        assert "mock-data.js" not in html
        assert "api-contract.js" not in html
        assert "app.js" not in html
    finally:
        _stop_test_server(server, thread)


def test_login_api_returns_success_for_seeded_demo_account():
    """FT-LOGIN-02: The login API should accept the seeded demo account."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post_login(base_url, "demo@moffatbay.com", "DemoPass1")

        assert status == 200
        assert payload["success"] is True
        assert payload["first_name"] == "Demo"
        assert isinstance(payload["customer_id"], int)
    finally:
        _stop_test_server(server, thread)


def test_login_api_returns_generic_error_for_invalid_password():
    """FT-LOGIN-03: An incorrect password should return a generic error."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post_login(base_url, "demo@moffatbay.com", "WrongPassword1")

        assert status == 401
        assert payload["success"] is False
        assert payload["reason"] == "Invalid email or password."
    finally:
        _stop_test_server(server, thread)
