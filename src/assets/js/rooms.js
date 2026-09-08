/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Client-side max-occupancy filter for the Rooms & Pricing page. Room capacity
values are hardcoded from sql/seed.sql RoomTypes data (no API call needed).
*/

"use strict";

function applyCapacityFilter() {
    const filter = document.getElementById("capacity-filter");
    const emptyHint = document.getElementById("capacity-filter-empty");
    if (!filter) return;

    const minGuests = Number(filter.value);
    const cards = document.querySelectorAll("#room-list .room-detail-card");
    let visibleCount = 0;

    cards.forEach((card) => {
        const maxOccupancy = Number(card.dataset.maxOccupancy || 0);
        const matches = minGuests === 0 || maxOccupancy >= minGuests;
        card.style.display = matches ? "" : "none";
        if (matches) visibleCount += 1;
    });

    if (emptyHint) {
        emptyHint.style.display = visibleCount === 0 ? "" : "none";
    }
}

document.addEventListener("DOMContentLoaded", () => {
    const filter = document.getElementById("capacity-filter");
    if (filter) {
        filter.addEventListener("change", applyCapacityFilter);
    }
});
