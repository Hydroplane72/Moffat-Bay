"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Single combined dev server exposing the landing, login, and registration
APIs on one address:port, with CORS enabled so index.html, login.html, and
register.html can also be opened directly via file:// and still call the API.

Run from the project root with:
    python src/api/startup_api.py

Then open:
    http://127.0.0.1:8000/
"""

from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

SRC_DIR = Path(__file__).resolve().parents[1]
API_DIR = Path(__file__).resolve().parent

# Allow `import api.helpers...` when this file is run directly as a script.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

load_dotenv(API_DIR / ".env")  # DB config can also be supplied via src/api/.env

from api.helpers.auth import verify_login  # noqa: E402
from api.helpers.registration import DUPLICATE_EMAIL_REASON, register_customer  # noqa: E402
from api.landing_api import get_db_connection, load_room_types_from_database  # noqa: E402

# One shared address:port so every page and API endpoint looks like a single service.
SERVER_HOST = os.getenv("MOFFAT_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("MOFFAT_SERVER_PORT", "8000"))

DB_HOST = os.getenv("MOFFAT_DB_HOST", "localhost")
DB_PORT = int(os.getenv("MOFFAT_DB_PORT", "3306"))
DB_NAME = os.getenv("MOFFAT_DB_NAME", "moffat_bay")


class ApiRequestHandler(SimpleHTTPRequestHandler):
    """Serve the site files and every API endpoint from one address:port."""

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

    def do_POST(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/auth/login":
            self._handle_login()
            return

        if request_path == "/api/auth/register":
            self._handle_register()
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

    def _handle_login(self):
        body = self._read_json_body()

        if body is None:
            self._send_json(400, {"success": False, "reason": "Invalid request body."})
            return

        email = body.get("email", "")
        password = body.get("password", "")

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Login API error: %s", exc)
            self._send_json(
                500,
                {"success": False, "reason": "Unable to sign in at this time."},
            )
            return

        try:
            result = verify_login(email, password, connection)
        finally:
            if connection.is_connected():
                connection.close()

        status_code = 200 if result.success else 401
        self._send_json(
            status_code,
            {
                "success": result.success,
                "reason": result.reason,
                "customer_id": result.customer_id,
                "first_name": result.first_name,
            },
        )

    def _handle_register(self):
        body = self._read_json_body()

        if body is None:
            self._send_json(400, {"success": False, "reason": "Invalid request body."})
            return

        email = body.get("email", "")
        phone = body.get("phone", "")
        first_name = body.get("first_name", "")
        last_name = body.get("last_name", "")
        password = body.get("password", "")

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Registration API error: %s", exc)
            self._send_json(
                500,
                {"success": False, "reason": "Unable to create an account at this time."},
            )
            return

        try:
            result = register_customer(email, phone, first_name, last_name, password, connection)
        finally:
            if connection.is_connected():
                connection.close()

        if result.success:
            status_code = 200
        elif result.reason == DUPLICATE_EMAIL_REASON:
            status_code = 409
        else:
            status_code = 400

        self._send_json(
            status_code,
            {
                "success": result.success,
                "reason": result.reason,
                "customer_id": result.customer_id,
                "first_name": result.first_name,
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
    return ThreadingHTTPServer((host, port), ApiRequestHandler)


def main():
    server = create_server()
    address, port = server.server_address[:2]

    print("=" * 68)
    print("MOFFAT BAY API SERVER (landing + login + registration)")
    print("=" * 68)
    print(f"Website:          http://{address}:{port}/")
    print(f"Room API:         http://{address}:{port}/api/landing/room-types")
    print(f"Login API:        http://{address}:{port}/api/auth/login")
    print(f"Registration API: http://{address}:{port}/api/auth/register")
    print(f"Database:         {DB_NAME} on {DB_HOST}:{DB_PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 68)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Moffat Bay API server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
