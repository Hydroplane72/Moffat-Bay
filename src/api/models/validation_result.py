"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result of validating a single input value.
"""

from dataclasses import dataclass


@dataclass
class ValidationResult:
    is_valid: bool
    reason: str
