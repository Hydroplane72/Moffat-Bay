/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Renders the reservation cart built on reservation.html, re-checks
availability as a final guard, and confirms the booking through the
reservation API.
*/

"use strict";

const RESERVATION_AUTH_SESSION_KEY = "mbl_session";
const CART_STORAGE_KEY = "mbl_reservation_cart";

function getAuthSession() {
    try {
        const raw = localStorage.getItem(RESERVATION_AUTH_SESSION_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (error) {
        return null;
    }
}

function loadCart() {
    try {
        const raw = sessionStorage.getItem(CART_STORAGE_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (error) {
        return null;
    }
}

function computeNights(checkIn, checkOut) {
    const nights = (new Date(checkOut) - new Date(checkIn)) / (1000 * 60 * 60 * 24);
    return Number.isFinite(nights) && nights > 0 ? nights : 0;
}

function showMessage(text, isError) {
    const messageEl = document.getElementById("summary-message");
    if (!messageEl) return;
    messageEl.textContent = text;
    messageEl.className = `message ${isError ? "error" : "success"}`;
}

function renderSummary(cart) {
    const grid = document.getElementById("summary-grid");
    const nights = computeNights(cart.checkIn, cart.checkOut);
    let total = 0;

    const roomLines = cart.rooms.map((room) => {
        const subtotal = nights * room.price_per_night * room.quantity;
        total += subtotal;
        return `<li class="receipt-line"><span>${room.quantity} x ${room.room_type_name} — $${room.price_per_night.toFixed(2)}/night</span><span>$${subtotal.toFixed(2)}</span></li>`;
    }).join("");

    grid.innerHTML = `
        <ul class="receipt-list">
            <li class="receipt-line"><span>Check-In</span><span>${cart.checkIn}</span></li>
            <li class="receipt-line"><span>Check-Out</span><span>${cart.checkOut} (${nights} night${nights === 1 ? "" : "s"})</span></li>
            <li class="receipt-line"><span>Guests</span><span>${cart.guests}</span></li>
            ${roomLines}
            <li class="receipt-line receipt-total"><span>Estimated Total</span><span>$${total.toFixed(2)}</span></li>
        </ul>
    `;
}

async function checkAvailability(cart) {
    const rooms = cart.rooms.map((room) => ({ room_type_id: room.room_type_id, quantity: room.quantity }));
    const response = await fetch(`${API_BASE_URL}/api/reservations/availability`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ check_in: cart.checkIn, check_out: cart.checkOut, rooms }),
    });
    return response.json();
}

async function confirmReservation(cart) {
    const rooms = cart.rooms.map((room) => ({ room_type_id: room.room_type_id, quantity: room.quantity }));
    const response = await fetch(`${API_BASE_URL}/api/reservations`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            customer_id: cart.customerId,
            guests: cart.guests,
            check_in: cart.checkIn,
            check_out: cart.checkOut,
            rooms,
        }),
    });
    return response.json();
}

document.addEventListener("DOMContentLoaded", async () => {
    const cart = loadCart();
    const controls = document.getElementById("summary-controls");
    const confirmButton = document.getElementById("confirm-reservation");
    const cancelButton = document.getElementById("cancel-reservation");

    if (!cart || !cart.rooms || cart.rooms.length === 0) {
        document.getElementById("summary-grid").innerHTML = "";
        showMessage("No reservation to review. Start a new booking from the Book page.", true);
        controls.style.display = "none";
        return;
    }

    renderSummary(cart);

    const availability = await checkAvailability(cart);
    if (!availability.ok) {
        showMessage(availability.reason, true);
        confirmButton.disabled = true;
    }

    cancelButton.addEventListener("click", () => {
        sessionStorage.removeItem(CART_STORAGE_KEY);
        window.location.href = "reservation.html";
    });

    confirmButton.addEventListener("click", async () => {
        const session = getAuthSession();
        if (!session || !session.firstName) {
            showMessage("Please log in before confirming your reservation.", true);
            return;
        }

        const recheck = await checkAvailability(cart);
        if (!recheck.ok) {
            showMessage(recheck.reason, true);
            confirmButton.disabled = true;
            return;
        }

        const result = await confirmReservation({ ...cart, customerId: session.customerId });
        if (result.success) {
            sessionStorage.removeItem(CART_STORAGE_KEY);
            showMessage(`Reservation confirmed! Confirmation #${result.reservation_id}.`, false);
            confirmButton.disabled = true;
            cancelButton.disabled = true;
        } else {
            showMessage(result.reason, true);
        }
    });
});
