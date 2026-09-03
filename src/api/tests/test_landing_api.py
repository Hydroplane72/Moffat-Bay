"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Two functional development tests for the Moffat Bay landing page.

Test 1 verifies that the production landing page is served with its required
navigation, call-to-action links, and landing JavaScript.

Test 2 verifies that the landing API can read the four seeded RoomTypes records
from the actual local MySQL database and return them as JSON.
"""

import json
import threading
from urllib.request import urlopen

from api.landing_api import create_server


def _start_test_server():
    server = create_server(host="127.0.0.1", port=0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread


def _stop_test_server(server, thread):
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)


def test_landing_page_loads_with_production_navigation_and_script():
    """FT-LP-01: The landing page should load and expose its primary actions."""
    server, thread = _start_test_server()

    try:
        url = f"http://127.0.0.1:{server.server_port}/"

        with urlopen(url, timeout=5) as response:
            html = response.read().decode("utf-8")
            status = response.status

        assert status == 200
        assert "Moffat Bay Lodge" in html
        assert 'href="reservation.html"' in html
        assert 'href="rooms.html"' in html
        assert 'id="landing-room-grid"' in html
        assert 'src="assets/js/landing.js"' in html
        assert "mock-data.js" not in html
        assert "api-contract.js" not in html
        assert "app.js" not in html
    finally:
        _stop_test_server(server, thread)


def test_landing_room_api_returns_seeded_room_types_from_database():
    """FT-LP-02: The API should return all four seeded room types from MySQL."""
    server, thread = _start_test_server()

    try:
        url = f"http://127.0.0.1:{server.server_port}/api/landing/room-types"

        with urlopen(url, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))
            status = response.status
            content_type = response.headers.get("Content-Type", "")

        assert status == 200
        assert content_type.startswith("application/json")
        assert [room["room_type_name"] for room in payload["room_types"]] == [
            "Double Full Beds",
            "Queen",
            "Double Queen Beds",
            "King",
        ]
        assert [room["price_per_night"] for room in payload["room_types"]] == [
            "120.00",
            "135.00",
            "150.00",
            "160.00",
        ]
    finally:
        _stop_test_server(server, thread)
