"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Development web server and login API for Moffat Bay Lodge.

The server hosts the files inside src/ and exposes a login endpoint that
checks guest email/password credentials against the shared MySQL database.
Kept as its own module (mirroring src/api/landing_api.py) so it can be run
and tested in isolation without touching another teammate's page/server.

Run from the project root with:
    python src/api/login_api.py

Then open:
    http://127.0.0.1:8001/login.html
"""

from __future__ import annotations

import json
import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


SRC_DIR = Path(__file__).resolve().parents[1]

# Allow `import api.helpers...` when this file is run directly as a script.
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from api.helpers.auth import verify_login  # noqa: E402

DB_HOST = os.getenv("MOFFAT_DB_HOST", "localhost")
DB_PORT = int(os.getenv("MOFFAT_DB_PORT", "3306"))
DB_USER = os.getenv("MOFFAT_DB_USER", "root")
DB_PASSWORD = os.getenv("MOFFAT_DB_PASSWORD", "")
DB_NAME = os.getenv("MOFFAT_DB_NAME", "moffat_bay")

SERVER_HOST = os.getenv("MOFFAT_LOGIN_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("MOFFAT_LOGIN_SERVER_PORT", "8001"))


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


class LoginRequestHandler(SimpleHTTPRequestHandler):
    """Serve the site files and the read/write login API."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(SRC_DIR), **kwargs)

    def do_GET(self):
        request_path = urlsplit(self.path).path

        # Backend source code and SQL files are not public static assets.
        if request_path.startswith("/api/") or request_path.startswith("/sql/"):
            self.send_error(404, "Not Found")
            return

        if request_path == "/":
            self.path = "/login.html"

        super().do_GET()

    def do_POST(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/auth/login":
            self._handle_login()
            return

        self.send_error(404, "Not Found")

    def list_directory(self, path):
        """Disable directory browsing."""
        self.send_error(404, "Not Found")
        return None

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
    return ThreadingHTTPServer((host, port), LoginRequestHandler)


def main():
    server = create_server()
    address, port = server.server_address[:2]

    print("=" * 68)
    print("MOFFAT BAY LOGIN PAGE SERVER")
    print("=" * 68)
    print(f"Website:    http://{address}:{port}/")
    print(f"Login API:  http://{address}:{port}/api/auth/login")
    print(f"Database:   {DB_NAME} on {DB_HOST}:{DB_PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 68)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Moffat Bay login page server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
