"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Login credential verification against the shared Customers table. 
Kept separate from the HTTP server so the logic can be unit tested on its own.
"""

from api.models.auth_result import AuthResult

GENERIC_INVALID_CREDENTIALS_REASON = "Invalid email or password."


def verify_login(email: str, password: str, connection) -> AuthResult:
    """Check an email/password pair against the Customers table.

    The same generic reason is returned for an unknown email and a wrong
    password so a caller cannot use the message to enumerate registered
    accounts.
    """
    if email is None or not email.strip():
        return AuthResult(success=False, reason="Email address is required.")

    if not password:
        return AuthResult(success=False, reason="Password is required.")

    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            """
            SELECT customer_id, first_name
            FROM Customers
            WHERE email = %s AND password_hash = SHA2(%s, 256)
            """,
            (email.strip(), password),
        )
        row = cursor.fetchone()
    finally:
        cursor.close()

    if row is None:
        return AuthResult(success=False, reason=GENERIC_INVALID_CREDENTIALS_REASON)

    return AuthResult(
        success=True,
        reason="Login successful.",
        customer_id=int(row["customer_id"]),
        first_name=str(row["first_name"]),
    )
