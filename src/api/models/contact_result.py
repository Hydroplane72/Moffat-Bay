"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result of submitting a contact/inquiry message.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ContactResult:
    success: bool
    reason: str
    message_id: Optional[int] = None
