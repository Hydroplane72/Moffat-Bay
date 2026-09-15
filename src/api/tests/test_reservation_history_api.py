"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Functional development tests for the reservation history API endpoint, using
the actual local MySQL database (seeded via sql/seed.sql).
"""

import json
import threading
from urllib.error import HTTPError
from urllib.request import urlopen

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


def _get(base_url, path):
    try:
        with urlopen(f"{base_url}{path}", timeout=5) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        return error.code, json.loads(error.read().decode("utf-8"))


def test_history_requires_customer_id():
    """FT-HIST-01: a missing customer_id should be rejected."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _get(base_url, "/api/reservations/history")

        assert status == 400
        assert "error" in payload
    finally:
        _stop_test_server(server, thread)


def test_history_returns_seeded_reservation_with_line_items():
    """FT-HIST-02: the seeded demo customer (id 1) has one past reservation with a line item."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _get(base_url, "/api/reservations/history?customer_id=1")

        assert status == 200
        reservations = payload["reservations"]
        assert len(reservations) >= 1

        entry = reservations[0]
        assert entry["check_in_date"] and entry["check_out_date"]
        assert float(entry["total_price"]) > 0
        assert len(entry["line_items"]) >= 1
        assert entry["line_items"][0]["room_number"]
    finally:
        _stop_test_server(server, thread)


def test_history_returns_empty_list_for_unknown_customer():
    """FT-HIST-03: a customer with no reservations should get an empty list, not an error."""
    server, thread = _start_test_server()

    try:
        base_url = f"http://127.0.0.1:{server.server_port}"
        status, payload = _get(base_url, "/api/reservations/history?customer_id=999999")

        assert status == 200
        assert payload["reservations"] == []
    finally:
        _stop_test_server(server, thread)
