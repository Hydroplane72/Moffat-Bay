"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result of an authentication attempt.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class AuthResult:
    success: bool
    reason: str
    customer_id: Optional[int] = None
    first_name: Optional[str] = None
