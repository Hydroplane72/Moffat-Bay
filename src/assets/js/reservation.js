/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Builds a multi-room-type reservation cart on the Book page: auto-selects the
room passed in from rooms.html, requires login before adding a room, checks
live availability via the reservation API, and hands the cart off to the
summary page.
*/

"use strict";

const RESERVATION_AUTH_SESSION_KEY = "mbl_session";
const CART_STORAGE_KEY = "mbl_reservation_cart";

let roomTypesById = {};
let cart = [];

function getAuthSession() {
    try {
        const raw = localStorage.getItem(RESERVATION_AUTH_SESSION_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (error) {
        return null;
    }
}

function showMessage(text, isError) {
    const messageEl = document.getElementById("reservation-message");
    if (!messageEl) return;
    messageEl.textContent = text;
    messageEl.className = `message ${isError ? "error" : "success"}`;
}

function clearMessage() {
    const messageEl = document.getElementById("reservation-message");
    if (!messageEl) return;
    messageEl.textContent = "";
    messageEl.className = "message";
}

function computeNights(checkIn, checkOut) {
    if (!checkIn || !checkOut) return 0;
    const nights = (new Date(checkOut) - new Date(checkIn)) / (1000 * 60 * 60 * 24);
    return Number.isFinite(nights) && nights > 0 ? nights : 0;
}

function updateAuthGatedVisibility() {
    const panel = document.getElementById("before-confirm-panel");
    const form = document.getElementById("reservation-form");
    const session = getAuthSession();
    const loggedIn = Boolean(session && session.firstName);

    if (panel) panel.style.display = loggedIn ? "none" : "";
    if (form) form.style.display = loggedIn ? "" : "none";
}

async function loadRoomTypes() {
    const select = document.getElementById("roomType");
    const response = await fetch(`${API_BASE_URL}/api/landing/room-types`);
    const payload = await response.json();

    select.innerHTML = "";
    roomTypesById = {};

    payload.room_types.forEach((roomType) => {
        roomTypesById[roomType.room_type_id] = roomType;
        const option = document.createElement("option");
        option.value = String(roomType.room_type_id);
        option.textContent = `${roomType.room_type_name} ($${roomType.price_per_night})`;
        select.appendChild(option);
    });

    preselectRoomFromQuery();
    updateRateHint();
}

function preselectRoomFromQuery() {
    const params = new URLSearchParams(window.location.search);
    const requestedName = params.get("room");
    if (!requestedName) return;

    const select = document.getElementById("roomType");
    const match = Object.values(roomTypesById).find((roomType) => roomType.room_type_name === requestedName);
    if (match) {
        select.value = String(match.room_type_id);
    }
}

function updateRateHint() {
    const select = document.getElementById("roomType");
    const hint = document.getElementById("room-rate-hint");
    const roomType = roomTypesById[Number(select.value)];
    if (hint && roomType) {
        hint.textContent = `${roomType.room_type_name} sleeps up to ${roomType.max_occupancy} guests at $${roomType.price_per_night} / night.`;
    }
}

function renderCart() {
    const list = document.getElementById("room-cart");
    const totalEl = document.getElementById("cart-total");
    const continueButton = document.getElementById("continue-to-summary");
    const nights = computeNights(getCheckIn(), getCheckOut());

    list.innerHTML = "";
    let total = 0;

    cart.forEach((item, index) => {
        const subtotal = nights * item.pricePerNight * item.quantity;
        total += subtotal;

        const li = document.createElement("li");
        li.className = "room-cart-item";

        const statusText = item.available === false
            ? `Unavailable (only ${item.availableCount} left)`
            : "Available";

        li.innerHTML = `
            <span>${item.quantity} x ${item.roomTypeName} — $${item.pricePerNight.toFixed(2)}/night</span>
            <span>Subtotal: $${subtotal.toFixed(2)}</span>
            <span class="${item.available === false ? "error" : ""}">${statusText}</span>
        `;

        const removeButton = document.createElement("button");
        removeButton.type = "button";
        removeButton.className = "btn btn-ghost";
        removeButton.textContent = "Remove";
        removeButton.addEventListener("click", () => {
            cart.splice(index, 1);
            renderCart();
            if (cart.length > 0) refreshAvailability();
        });
        li.appendChild(removeButton);

        list.appendChild(li);
    });

    totalEl.textContent = cart.length > 0 ? `Estimated Total: $${total.toFixed(2)} (${nights} night${nights === 1 ? "" : "s"})` : "";

    const allAvailable = cart.every((item) => item.available !== false);
    continueButton.disabled = !(cart.length > 0 && allAvailable && nights > 0);
}

function getCheckIn() {
    return document.getElementById("checkIn").value;
}

function getCheckOut() {
    return document.getElementById("checkOut").value;
}

async function checkAvailability(checkIn, checkOut, rooms) {
    const response = await fetch(`${API_BASE_URL}/api/reservations/availability`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ check_in: checkIn, check_out: checkOut, rooms }),
    });
    return response.json();
}

async function refreshAvailability() {
    const checkIn = getCheckIn();
    const checkOut = getCheckOut();
    if (!checkIn || !checkOut || cart.length === 0) return;

    const rooms = cart.map((item) => ({ room_type_id: item.roomTypeId, quantity: item.quantity }));
    const result = await checkAvailability(checkIn, checkOut, rooms);

    cart.forEach((item) => {
        const detail = result.details.find((d) => d.room_type_id === item.roomTypeId);
        item.available = detail ? detail.ok : false;
        item.availableCount = detail ? detail.available_count : 0;
    });

    renderCart();
}

async function handleAddRoom() {
    clearMessage();

    const session = getAuthSession();
    if (!session || !session.firstName) {
        showMessage("Please log in or register before adding rooms to your reservation.", true);
        return;
    }

    const checkIn = getCheckIn();
    const checkOut = getCheckOut();
    if (!checkIn || !checkOut || checkOut <= checkIn) {
        showMessage("Choose a check-in date and a later check-out date first.", true);
        return;
    }

    const select = document.getElementById("roomType");
    const roomTypeId = Number(select.value);
    const roomType = roomTypesById[roomTypeId];
    const quantity = Math.max(1, Number(document.getElementById("roomQty").value) || 1);

    const existingLine = cart.find((item) => item.roomTypeId === roomTypeId);
    const mergedRooms = cart
        .filter((item) => item.roomTypeId !== roomTypeId)
        .map((item) => ({ room_type_id: item.roomTypeId, quantity: item.quantity }));
    mergedRooms.push({ room_type_id: roomTypeId, quantity: (existingLine ? existingLine.quantity : 0) + quantity });

    const result = await checkAvailability(checkIn, checkOut, mergedRooms);
    const detail = result.details.find((d) => d.room_type_id === roomTypeId);

    if (!result.ok || !detail || !detail.ok) {
        showMessage(
            detail ? `Only ${detail.available_count} ${roomType.room_type_name} room(s) are available for those dates.` : result.reason,
            true,
        );
        return;
    }

    if (existingLine) {
        existingLine.quantity += quantity;
    } else {
        cart.push({
            roomTypeId,
            roomTypeName: roomType.room_type_name,
            quantity,
            pricePerNight: Number(roomType.price_per_night),
            available: true,
            availableCount: detail.available_count,
        });
    }

    await refreshAvailability();
}

function handleContinueToSummary() {
    const session = getAuthSession();
    if (!session || !session.firstName) {
        showMessage("Please log in or register before confirming your reservation.", true);
        return;
    }

    const payload = {
        customerId: session.customerId,
        guests: Number(document.getElementById("guests").value),
        checkIn: getCheckIn(),
        checkOut: getCheckOut(),
        rooms: cart.map((item) => ({
            room_type_id: item.roomTypeId,
            room_type_name: item.roomTypeName,
            quantity: item.quantity,
            price_per_night: item.pricePerNight,
        })),
    };

    sessionStorage.setItem(CART_STORAGE_KEY, JSON.stringify(payload));
    window.location.href = "reservation-summary.html";
}

document.addEventListener("DOMContentLoaded", () => {
    updateAuthGatedVisibility();
    loadRoomTypes();

    document.getElementById("roomType").addEventListener("change", updateRateHint);
    document.getElementById("add-room").addEventListener("click", handleAddRoom);
    document.getElementById("continue-to-summary").addEventListener("click", handleContinueToSummary);
    document.getElementById("checkIn").addEventListener("change", refreshAvailability);
    document.getElementById("checkOut").addEventListener("change", refreshAvailability);
});
