"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result of creating a reservation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ReservationResult:
    success: bool
    reason: str
    reservation_id: Optional[int] = None
    total_price: Optional[str] = None
