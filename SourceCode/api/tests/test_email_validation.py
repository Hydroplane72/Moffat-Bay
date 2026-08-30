"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Tests for api.helpers.email_validation.
"""

from api.helpers.email_validation import validate_email


def test_valid_email_returns_true():
    result = validate_email("guest@example.com")

    assert result.is_valid is True
    assert result.reason == "Email address is valid."


def test_missing_dot_in_domain_returns_false():
    result = validate_email("guest@examplecom")

    assert result.is_valid is False
    assert "format" in result.reason


def test_missing_at_sign_returns_false():
    result = validate_email("guest.example.com")

    assert result.is_valid is False
    assert "format" in result.reason


def test_empty_email_returns_false_with_required_reason():
    result = validate_email("")

    assert result.is_valid is False
    assert result.reason == "Email address is required."


def test_whitespace_only_email_returns_false_with_required_reason():
    result = validate_email("   ")

    assert result.is_valid is False
    assert result.reason == "Email address is required."


def test_email_with_surrounding_whitespace_is_trimmed_and_valid():
    result = validate_email("  guest@example.com  ")

    assert result.is_valid is True
