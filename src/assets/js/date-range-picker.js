/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Wires the Check-In/Check-Out fields to a single shared Flatpickr range
calendar (loaded via CDN) so dates can only be picked, never typed.
*/

"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const checkIn = document.getElementById("checkIn");
    const checkOut = document.getElementById("checkOut");

    if (!checkIn || !checkOut || typeof flatpickr === "undefined") return;

    // Flatpickr updates .value directly without firing a native "change" event.
    const notifyChange = () => {
        checkIn.dispatchEvent(new Event("change", { bubbles: true }));
        checkOut.dispatchEvent(new Event("change", { bubbles: true }));
    };

    flatpickr(checkIn, {
        mode: "range",
        dateFormat: "Y-m-d",
        minDate: "today",
        plugins: [new rangePlugin({ input: checkOut })],
        onClose: notifyChange,
    });
});
