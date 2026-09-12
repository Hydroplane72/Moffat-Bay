"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Development web server and contact API for the Moffat Bay Lodge about page.

The server hosts the files inside src/ and exposes a write-only endpoint that
saves guest inquiries from the about page's "Send an Inquiry" form into the
shared MySQL database. Kept as its own module (mirroring src/api/login_api.py)
so it can be run and tested in isolation without touching another teammate's
page/server.

Run from the project root with:
    python src/api/about_api.py

Then open:
    http://127.0.0.1:8004/about.html
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

from api.helpers.contact import submit_contact_message  # noqa: E402

DB_HOST = os.getenv("MOFFAT_DB_HOST", "localhost")
DB_PORT = int(os.getenv("MOFFAT_DB_PORT", "3306"))
DB_USER = os.getenv("MOFFAT_DB_USER", "root")
DB_PASSWORD = os.getenv("MOFFAT_DB_PASSWORD", "")
DB_NAME = os.getenv("MOFFAT_DB_NAME", "moffat_bay")

SERVER_HOST = os.getenv("MOFFAT_ABOUT_SERVER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("MOFFAT_ABOUT_SERVER_PORT", "8004"))


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


class AboutRequestHandler(SimpleHTTPRequestHandler):
    """Serve the about page files and its write-only contact API."""

    def __init__(self, *args, directory=None, **kwargs):
        super().__init__(*args, directory=str(SRC_DIR), **kwargs)

    def do_GET(self):
        request_path = urlsplit(self.path).path

        # Backend source code and SQL files are not public static assets.
        if request_path.startswith("/api/") or request_path.startswith("/sql/"):
            self.send_error(404, "Not Found")
            return

        if request_path == "/":
            self.path = "/about.html"

        super().do_GET()

    def do_POST(self):
        request_path = urlsplit(self.path).path

        if request_path == "/api/contact":
            self._handle_contact_message()
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

    def _handle_contact_message(self):
        body = self._read_json_body()

        if body is None:
            self._send_json(400, {"success": False, "reason": "Invalid request body."})
            return

        name = body.get("name", "")
        email = body.get("email", "")
        subject = body.get("subject", "")
        message = body.get("message", "")

        try:
            connection = get_db_connection()
        except Exception as exc:  # Server logs detail; client receives a safe message.
            self.log_error("Contact API error: %s", exc)
            self._send_json(
                500,
                {"success": False, "reason": "Unable to send your message at this time."},
            )
            return

        try:
            result = submit_contact_message(name, email, subject, message, connection)
        finally:
            if connection.is_connected():
                connection.close()

        status_code = 200 if result.success else 400
        self._send_json(
            status_code,
            {
                "success": result.success,
                "reason": result.reason,
                "message_id": result.message_id,
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
    return ThreadingHTTPServer((host, port), AboutRequestHandler)


def main():
    server = create_server()
    address, port = server.server_address[:2]

    print("=" * 68)
    print("MOFFAT BAY ABOUT PAGE SERVER")
    print("=" * 68)
    print(f"Website:     http://{address}:{port}/")
    print(f"Contact API: http://{address}:{port}/api/contact")
    print(f"Database:    {DB_NAME} on {DB_HOST}:{DB_PORT}")
    print("Press Ctrl+C to stop the server.")
    print("=" * 68)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Moffat Bay about page server...")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
