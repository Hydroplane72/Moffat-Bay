"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Guest account creation against the shared Customers table. Kept separate from
the HTTP server so the logic can be unit tested on its own.
"""

import re

from api.helpers.email_validation import validate_email
from api.models.auth_result import AuthResult

DUPLICATE_EMAIL_REASON = "Email already exists in the database."

# Requires 8+ characters with at least one uppercase, one lowercase, and one digit
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")


def register_customer(
    email: str,
    phone: str,
    first_name: str,
    last_name: str,
    password: str,
    connection,
) -> AuthResult:
    """Validate guest registration input and insert a new Customers row."""
    if not first_name or not first_name.strip():
        return AuthResult(success=False, reason="First name is required.")

    if not last_name or not last_name.strip():
        return AuthResult(success=False, reason="Last name is required.")

    if not phone or not phone.strip():
        return AuthResult(success=False, reason="Telephone number is required.")

    email_check = validate_email(email)
    if not email_check.is_valid:
        return AuthResult(success=False, reason=email_check.reason)

    if not password or not PASSWORD_PATTERN.match(password):
        return AuthResult(
            success=False,
            reason=(
                "Password must be at least 8 characters with one uppercase "
                "letter, one lowercase letter, and one number."
            ),
        )

    normalized_email = email.strip()
    cursor = connection.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT customer_id FROM Customers WHERE email = %s",
            (normalized_email,),
        )
        if cursor.fetchone() is not None:
            return AuthResult(success=False, reason=DUPLICATE_EMAIL_REASON)

        # A race against another request can still hit the UNIQUE constraint.
        try:
            cursor.execute(
                """
                INSERT INTO Customers (first_name, last_name, email, phone, password_hash)
                VALUES (%s, %s, %s, %s, SHA2(%s, 256))
                """,
                (
                    first_name.strip(),
                    last_name.strip(),
                    normalized_email,
                    phone.strip(),
                    password,
                ),
            )
        except Exception as exc:
            import mysql.connector

            if isinstance(exc, mysql.connector.errors.IntegrityError):
                return AuthResult(success=False, reason=DUPLICATE_EMAIL_REASON)
            raise

        connection.commit()
        new_customer_id = cursor.lastrowid
    finally:
        cursor.close()

    return AuthResult(
        success=True,
        reason="Registration successful.",
        customer_id=int(new_customer_id),
        first_name=first_name.strip(),
    )
