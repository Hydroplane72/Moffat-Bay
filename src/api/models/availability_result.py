"""
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Result of checking whether requested room types/quantities are free for a
date range.
"""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RoomTypeAvailability:
    room_type_id: int
    requested: int
    available_count: int
    ok: bool


@dataclass
class AvailabilityResult:
    ok: bool
    reason: str
    details: List[RoomTypeAvailability] = field(default_factory=list)
    # Room ids assigned per room_type_id, only populated on a successful check
    # so create_reservation() can reuse them without re-querying.
    assigned_room_ids: Optional[dict] = None
