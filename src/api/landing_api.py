"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Development web server and landing page API for Moffat Bay Lodge.

The server hosts the files inside src/ and exposes a read-only endpoint that
loads room types and nightly pricing from the shared MySQL database.

Run from the project root with:
    python src/api/landing_api.py

Then open:
    http://127.0.0.1:8000/
"""

from __future__ import annotations

import json
import os
from decimal import Decimal
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


SRC_DIR = Path(__file__).resolve().parents[1]

DB_HOST = os.getenv("MOFFAT_DB_HOST", "localhost")
DB_PORT = int(os.getenv("MOFFAT_DB_PORT", "3306"))
DB_USER = os.getenv("MOFFAT_DB_USER", "root")
DB_PASSWORD = os.getenv("MOFFAT_DB_PASSWORD", "")
DB_NAME = os.getenv("MOFFAT_DB_NAME", "moffat_bay")

SERVER_HOST = os.getenv("MOFFAT_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("MOFFAT_SERVER_PORT", "8000"))


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


def fetch_room_types(connection) -> list[dict]:
    """Read the room types shown on the landing page from MySQL."""
    query = """
        SELECT
            room_type_id,
            room_type_name,
            price_per_night,
            max_occupancy
        FROM RoomTypes
        ORDER BY room_type_id;
    """

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        cursor.close()

    room_types = []

    for row in rows:
        price = row["price_per_night"]

        if isinstance(price, Decimal):
            price_text = f"{price:.2f}"
        else:
            price_text = f"{float(price):.2f}"

        room_types.append(
            {
                "room_type_id": int(row["room_type_id"]),
                "room_type_name": str(row["room_type_name"]),
                "price_per_night": price_text,
                "max_occupancy": int(row["max_occupancy"]),
            }
        )

    return room_types


def load_room_types_from_database() -> list[dict]:
    """Open a connection, load room types, and always close the connection."""
    connection = get_db_connection()

    try:
        return fetch_room_types(connection)
    finally:
        if connection.is_connected():
            connection.close()


class LandingRequestHandler(SimpleHTTPRequestHandler):
    """Serve the landing page files and its read-only room type API."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(SRC_DIR), **kwargs)

    def do_GET(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/landing/room-types":
            self._send_room_types()
            return

        # Backend source code and SQL files are not public static assets.
        if request_path.startswith("/api/") or request_path.startswith("/sql/"):
            self.send_error(404, "Not Found")
            return

        if request_path == "/":
            self.path = "/index.html"

        super().do_GET()

    def list_directory(self, path):
        """Disable directory browsing."""
        self.send_error(404, "Not Found")
        return None

    def _send_room_types(self):
        try:
            room_types = load_room_types_from_database()
            self._send_json(200, {"room_types": room_types})
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Landing API error: %s", exc)
            self._send_json(
                500,
                {"error": "Unable to load room information at this time."},
            )

    def _send_json(self, status_code: int, payload: dict):
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = SERVER_HOST, port: int = SERVER_PORT):
    """Create the threaded HTTP server. A port of 0 selects a free test port."""
    return ThreadingHTTPServer((host, port), LandingRequestHandler)


def main():
    server = create_server()
    address, port = server.server_address[:2]

    print("=" * 68)
    print("MOFFAT BAY LANDING PAGE SERVER")
    print("=" * 68)
    print(f"Website:  http://{address}:{port}/")
    print(f"Room API: http://{address}:{port}/api/landing/room-types")
    print(f"Database: {DB_NAME} on {DB_HOST}:{DB_PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 68)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Moffat Bay landing page server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
