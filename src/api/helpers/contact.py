"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Guest contact/inquiry submission against the shared ContactMessages table.
Kept separate from the HTTP server so the logic can be unit tested on its own.
"""

from api.helpers.email_validation import validate_email
from api.models.contact_result import ContactResult


def submit_contact_message(name: str, email: str, subject: str, message: str, connection) -> ContactResult:
    """Validate an inquiry's fields and insert a new ContactMessages row."""
    if not name or not name.strip():
        return ContactResult(success=False, reason="Full name is required.")

    email_check = validate_email(email)
    if not email_check.is_valid:
        return ContactResult(success=False, reason=email_check.reason)

    if not subject or not subject.strip():
        return ContactResult(success=False, reason="Subject is required.")

    if not message or not message.strip():
        return ContactResult(success=False, reason="Message is required.")

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO ContactMessages (name, email, subject, message)
            VALUES (%s, %s, %s, %s)
            """,
            (name.strip(), email.strip(), subject.strip(), message.strip()),
        )
        connection.commit()
        new_message_id = cursor.lastrowid
    finally:
        cursor.close()

    return ContactResult(
        success=True,
        reason="Your message has been sent.",
        message_id=int(new_message_id),
    )
