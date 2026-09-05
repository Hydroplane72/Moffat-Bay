"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Functional development tests for the registration API endpoint, using the
actual local MySQL database. Inserted test rows are deleted after each test.
"""

import json
import threading
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from api.newregistration_api import create_server, get_db_connection


def _start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_test_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def _post_register(base_url, payload):
    request = Request(
        f"{base_url}/api/auth/register",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urlopen(request, timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def _delete_customer(email):
    connection = get_db_connection()

    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Customers WHERE email = %s", (email,))
        connection.commit()
        cursor.close()
    finally:
        if connection.is_connected():
            connection.close()


def _valid_payload(email):
    return {
        "email": email,
        "phone": "555-123-4567",
        "first_name": "Test",
        "last_name": "Guest",
        "password": "TestPass1",
    }


def test_registration_api_creates_account_for_new_email():
    """FT-REGISTER-01: A new email should be registered successfully."""
    server, thread = _start_test_server()
    email = f"test-register-{time.time_ns()}@example.com"

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _post_register(base_url, _valid_payload(email))

        assert status == 200
        assert payload["success"] is True
        assert payload["first_name"] == "Test"
        assert isinstance(payload["customer_id"], int)
    finally:
        _stop_test_server(server, thread)
        _delete_customer(email)


def test_registration_api_rejects_duplicate_email():
    """FT-REGISTER-02: Registering the same email twice should fail with 409."""
    server, thread = _start_test_server()
    email = f"test-register-dup-{time.time_ns()}@example.com"

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        first_status, _ = _post_register(base_url, _valid_payload(email))
        assert first_status == 200

        status, payload = _post_register(base_url, _valid_payload(email))

        assert status == 409
        assert payload["success"] is False
        assert payload["reason"] == "Email already exists in the database."
    finally:
        _stop_test_server(server, thread)
        _delete_customer(email)


def test_registration_api_rejects_invalid_email_format():
    """FT-REGISTER-03: A malformed email should return a 400 validation error."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        payload = _valid_payload("not-an-email")
        status, response = _post_register(base_url, payload)

        assert status == 400
        assert response["success"] is False
    finally:
        _stop_test_server(server, thread)


def test_registration_api_rejects_weak_password():
    """FT-REGISTER-04: A password that fails the strength rule should return a 400."""
    server, thread = _start_test_server()
    email = f"test-register-weak-{time.time_ns()}@example.com"

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        payload = _valid_payload(email)
        payload["password"] = "weak"
        status, response = _post_register(base_url, payload)

        assert status == 400
        assert response["success"] is False
    finally:
        _stop_test_server(server, thread)


def test_registration_api_rejects_missing_required_field():
    """FT-REGISTER-05: A missing required field should return a 400."""
    server, thread = _start_test_server()
    email = f"test-register-missing-{time.time_ns()}@example.com"

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        payload = _valid_payload(email)
        payload["first_name"] = ""
        status, response = _post_register(base_url, payload)

        assert status == 400
        assert response["success"] is False
    finally:
        _stop_test_server(server, thread)
