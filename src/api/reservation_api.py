"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Development web server and reservation API for Moffat Bay Lodge. Exposes an
availability check (backed by the get_room_availability stored procedure)
and reservation creation.

Run from the project root with:
    python src/api/reservation_api.py

Then open:
    http://127.0.0.1:8003/
"""

from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from dotenv import load_dotenv

SRC_DIR = Path(__file__).resolve().parents[1]
API_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

load_dotenv(API_DIR / ".env")  # DB config can also be supplied via src/api/.env

from api.helpers.reservation import check_room_availability, create_reservation, get_reservation_history  # noqa: E402

DB_HOST = os.getenv("MOFFAT_DB_HOST", "localhost")
DB_PORT = int(os.getenv("MOFFAT_DB_PORT", "3306"))
DB_USER = os.getenv("MOFFAT_DB_USER", "root")
DB_PASSWORD = os.getenv("MOFFAT_DB_PASSWORD", "")
DB_NAME = os.getenv("MOFFAT_DB_NAME", "moffat_bay")

SERVER_HOST = os.getenv("MOFFAT_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("MOFFAT_RESERVATION_SERVER_PORT", "8003"))


def get_db_connection():
    """Create and return a MySQL connection using environment-based settings."""
    try:
        import mysql.connector
    except ImportError as exc:
        raise RuntimeError(
            "mysql-connector-python is required. Install it with "
            "'python -m pip install mysql-connector-python'."
        ) from exc

    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def _serialize_history_entry(entry):
    return {
        "reservation_id": entry.reservation_id,
        "check_in_date": entry.check_in_date.isoformat(),
        "check_out_date": entry.check_out_date.isoformat(),
        "num_guests": entry.num_guests,
        "total_price": f"{entry.total_price:.2f}",
        "status": entry.status,
        "line_items": [
            {
                "room_number": item.room_number,
                "room_type_name": item.room_type_name,
                "nightly_rate": f"{item.nightly_rate:.2f}",
                "nights": item.nights,
                "subtotal": f"{item.subtotal:.2f}",
            }
            for item in entry.line_items
        ],
    }


class ReservationRequestHandler(SimpleHTTPRequestHandler):
    """Serve the site files and the reservation availability/create API."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(SRC_DIR), **kwargs)

    def do_GET(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/reservations/history":
            self._send_reservation_history()
            return

        super().do_GET()

    def do_POST(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/reservations/availability":
            self._handle_availability()
            return

        if request_path == "/api/reservations":
            self._handle_create_reservation()
            return

        self.send_error(404, "Not Found")

    def do_OPTIONS(self):
        # Browsers preflight cross-origin POSTs, e.g. pages opened via file://.
        self.send_response(204)
        self._send_cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def list_directory(self, path):
        """Disable directory browsing."""
        self.send_error(404, "Not Found")
        return None

    def _send_reservation_history(self):
        query = parse_qs(urlsplit(self.path).query)
        customer_id = query.get("customer_id", [None])[0]

        if customer_id is None or not customer_id.isdigit():
            self._send_json(400, {"error": "A valid customer_id is required."})
            return

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Reservation history API error: %s", exc)
            self._send_json(500, {"error": "Unable to load reservation history at this time."})
            return

        try:
            entries = get_reservation_history(connection, customer_id)
        finally:
            if connection.is_connected():
                connection.close()

        self._send_json(200, {"reservations": [_serialize_history_entry(entry) for entry in entries]})

    def _handle_availability(self):
        body = self._read_json_body()

        if body is None:
            self._send_json(400, {"ok": False, "reason": "Invalid request body."})
            return

        check_in = body.get("check_in")
        check_out = body.get("check_out")
        rooms = body.get("rooms")

        if not isinstance(rooms, list):
            self._send_json(400, {"ok": False, "reason": "A list of rooms is required."})
            return

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Reservation API error: %s", exc)
            self._send_json(500, {"ok": False, "reason": "Unable to check availability at this time."})
            return

        try:
            result = check_room_availability(connection, check_in, check_out, rooms)
        finally:
            if connection.is_connected():
                connection.close()

        self._send_json(
            200,
            {
                "ok": result.ok,
                "reason": result.reason,
                "details": [
                    {
                        "room_type_id": detail.room_type_id,
                        "requested": detail.requested,
                        "available_count": detail.available_count,
                        "ok": detail.ok,
                    }
                    for detail in result.details
                ],
            },
        )

    def _handle_create_reservation(self):
        body = self._read_json_body()

        if body is None:
            self._send_json(400, {"success": False, "reason": "Invalid request body."})
            return

        customer_id = body.get("customer_id")
        guests = body.get("guests")
        check_in = body.get("check_in")
        check_out = body.get("check_out")
        rooms = body.get("rooms")

        if not isinstance(rooms, list):
            self._send_json(400, {"success": False, "reason": "A list of rooms is required."})
            return

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Reservation API error: %s", exc)
            self._send_json(500, {"success": False, "reason": "Unable to create a reservation at this time."})
            return

        try:
            result = create_reservation(connection, customer_id, guests, check_in, check_out, rooms)
        finally:
            if connection.is_connected():
                connection.close()

        status_code = 200 if result.success else 400

        self._send_json(
            status_code,
            {
                "success": result.success,
                "reason": result.reason,
                "reservation_id": result.reservation_id,
                "total_price": result.total_price,
            },
        )

    def _read_json_body(self, max_bytes: int = 8192):
        """Read and parse a bounded JSON request body, returning None on failure."""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
        except ValueError:
            return None

        if content_length <= 0 or content_length > max_bytes:
            return None

        raw_body = self.rfile.read(content_length)

        try:
            parsed = json.loads(raw_body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return None

        return parsed if isinstance(parsed, dict) else None

    def _send_cors_headers(self):
        # Lets pages opened directly via file:// (origin "null") call this API.
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _send_json(self, status_code: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = SERVER_HOST, port: int = SERVER_PORT):
    """Create the threaded HTTP server. A port of 0 selects a free test port."""
    return ThreadingHTTPServer((host, port), ReservationRequestHandler)


def main():
    server = create_server()
    address, port = server.server_address[:2]

    print("=" * 68)
    print("MOFFAT BAY RESERVATION API SERVER")
    print("=" * 68)
    print(f"Website:             http://{address}:{port}/")
    print(f"Availability API:    http://{address}:{port}/api/reservations/availability")
    print(f"Create Reservation:  http://{address}:{port}/api/reservations")
    print(f"Reservation History: http://{address}:{port}/api/reservations/history")
    print(f"Database:            {DB_NAME} on {DB_HOST}:{DB_PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 68)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Moffat Bay reservation API server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
