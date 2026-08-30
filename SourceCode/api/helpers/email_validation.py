"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Reusable email format validation helper for the Moffat Bay Lodge API.
"""

import re

from api.models.validation_result import ValidationResult

# Matches "text@domain.tld" - requires a "." between the domain and a letters-only extension
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")


def validate_email(email: str) -> ValidationResult:
    """Validate an email address's format and return a ValidationResult."""
    if email is None or not email.strip():
        return ValidationResult(is_valid=False, reason="Email address is required.")

    if EMAIL_PATTERN.match(email.strip()):
        return ValidationResult(is_valid=True, reason="Email address is valid.")

    return ValidationResult(
        is_valid=False,
        reason="Email address must be in the format name@domain.tld (e.g. you@example.com).",
    )
