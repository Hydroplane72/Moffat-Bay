/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Landing page behavior for Moffat Bay Lodge. This file controls the responsive
navigation menu and loads room type/pricing data from the landing page API.
*/

"use strict";

const ROOM_DESCRIPTIONS = {
    "Double Full Beds": "Comfortable space for families and small groups.",
    "Queen": "A relaxing choice for couples or solo travelers.",
    "Double Queen Beds": "Extra room for families and larger travel groups.",
    "King": "A spacious option for guests who want added comfort."
};

function setupMobileNavigation() {
    const menuToggle = document.getElementById("menu-toggle");
    const mainNav = document.getElementById("main-nav");

    if (!menuToggle || !mainNav) {
        return;
    }

    menuToggle.addEventListener("click", () => {
        const isOpen = mainNav.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    mainNav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            mainNav.classList.remove("open");
            menuToggle.setAttribute("aria-expanded", "false");
        });
    });
}

function formatNightlyRate(value) {
    const numericValue = Number(value);

    if (!Number.isFinite(numericValue)) {
        return "Rate unavailable";
    }

    return `${new Intl.NumberFormat("en-US", {
        style: "currency",
        currency: "USD",
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(numericValue)} / night`;
}

function createTextElement(tagName, className, text) {
    const element = document.createElement(tagName);

    if (className) {
        element.className = className;
    }

    element.textContent = text;
    return element;
}

function createRoomCard(room, index) {
    const article = document.createElement("article");
    article.className = "card";

    const roomName = String(room.room_type_name || "Room");
    const maxOccupancy = Number(room.max_occupancy);
    const description = ROOM_DESCRIPTIONS[roomName]
        || `Comfortable lodging for up to ${Number.isFinite(maxOccupancy) ? maxOccupancy : "several"} guests.`;

    article.appendChild(
        createTextElement("p", "card-number", String(index + 1).padStart(2, "0"))
    );
    article.appendChild(createTextElement("h3", "", roomName));
    article.appendChild(createTextElement("p", "", description));
    article.appendChild(
        createTextElement("p", "price", formatNightlyRate(room.price_per_night))
    );

    const selectLink = document.createElement("a");
    selectLink.className = "card-link";
    selectLink.href = `reservation.html?room=${encodeURIComponent(roomName)}`;
    selectLink.textContent = "Select Room →";
    article.appendChild(selectLink);

    return article;
}

async function loadRoomTypes() {
    const roomGrid = document.getElementById("landing-room-grid");
    const message = document.getElementById("room-data-message");

    if (!roomGrid) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/landing/room-types`, {
            method: "GET",
            headers: {
                "Accept": "application/json"
            }
        });

        if (!response.ok) {
            throw new Error(`Room API returned HTTP ${response.status}.`);
        }

        const payload = await response.json();

        if (!payload || !Array.isArray(payload.room_types) || payload.room_types.length === 0) {
            throw new Error("Room API returned no room types.");
        }

        const fragment = document.createDocumentFragment();
        payload.room_types.forEach((room, index) => {
            fragment.appendChild(createRoomCard(room, index));
        });

        roomGrid.replaceChildren(fragment);
        roomGrid.dataset.source = "database";

        if (message) {
            message.className = "message";
            message.textContent = "";
        }
    } catch (error) {
        console.error("Unable to load live room data:", error);

        // The HTML contains safe fallback room information, so visitors can
        // still browse the page if the API or database is temporarily offline.
        roomGrid.dataset.source = "fallback";

        if (message) {
            message.className = "message error";
            message.textContent = "Live room pricing is temporarily unavailable. Standard room information is shown above.";
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    setupMobileNavigation();
    loadRoomTypes();
});
