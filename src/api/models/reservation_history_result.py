"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result shapes for a customer's past reservations and the room line items
that make up each reservation's total.
"""

from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal
from typing import List


@dataclass
class ReservationHistoryLineItem:
    room_number: str
    room_type_name: str
    nightly_rate: Decimal
    nights: int
    subtotal: Decimal


@dataclass
class ReservationHistoryEntry:
    reservation_id: int
    check_in_date: date
    check_out_date: date
    num_guests: int
    total_price: Decimal
    status: str
    line_items: List[ReservationHistoryLineItem] = field(default_factory=list)
