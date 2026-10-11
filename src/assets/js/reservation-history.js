
/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Requires a logged-in guest, loads their past reservations from the
reservation history API, and renders them as a table where clicking a row
expands to show the room line items behind that stay's total.
*/

"use strict";

const HISTORY_AUTH_SESSION_KEY = "mbl_session";

function getHistoryAuthSession() {
    try {
        const raw = localStorage.getItem(HISTORY_AUTH_SESSION_KEY);
        return raw ? JSON.parse(raw) : null;
    } catch (error) {
        return null;
    }
}

function showHistoryMessage(text, isError) {
    const messageEl = document.getElementById("history-message");
    if (!messageEl) return;
    messageEl.textContent = text;
    messageEl.className = text ? `message ${isError ? "error" : "success"}` : "message";
}

async function fetchReservationHistory(customerId) {
    const response = await fetch(`${API_BASE_URL}/api/reservations/history?customer_id=${customerId}`);
    const payload = await response.json().catch(() => ({}));
    if (!response.ok || payload.error) {
        throw new Error(payload.error || payload.reason || "Unable to load reservation history at this time.");
    }
    return payload;
}

function buildLineItemsTable(lineItems) {
    const rows = lineItems.map((item) => `
        <tr>
            <td>${item.room_type_name}</td>
            <td>${item.room_number}</td>
            <td>$${item.nightly_rate}</td>
            <td>${item.nights}</td>
            <td>$${item.subtotal}</td>
        </tr>
    `).join("");

    return `
        <div class="history-line-items-scroll" role="region" aria-label="Reservation room details" tabindex="0">
            <table class="history-line-items">
                <thead>
                    <tr><th>Room Type</th><th>Room</th><th>Nightly Rate</th><th>Nights</th><th>Subtotal</th></tr>
                </thead>
                <tbody>${rows}</tbody>
            </table>
        </div>
    `;
}

function renderHistory(reservations) {
    const tbody = document.getElementById("history-table-body");
    tbody.innerHTML = "";

    reservations.forEach((reservation) => {
        const summaryRow = document.createElement("tr");
        summaryRow.className = "history-row";
        summaryRow.innerHTML = `
            <td>${reservation.check_in_date}</td>
            <td>${reservation.check_out_date}</td>
            <td>$${reservation.total_price}</td>
        `;

        const detailRow = document.createElement("tr");
        detailRow.className = "history-detail-row";
        const detailCell = document.createElement("td");
        detailCell.colSpan = 3;
        detailCell.innerHTML = buildLineItemsTable(reservation.line_items);
        detailRow.appendChild(detailCell);

        summaryRow.addEventListener("click", () => {
            detailRow.classList.toggle("open");
        });

        tbody.append(summaryRow, detailRow);
    });
}

let allHistoryReservations = [];

function applyHistoryFilters(event) {
    if (event) event.preventDefault();
    const from = document.getElementById("history-from").value;
    const to = document.getElementById("history-to").value;
    if (from && to && from > to) {
        document.getElementById("history-table-body").innerHTML = "";
        showHistoryMessage("The start date must be on or before the end date.", true);
        return;
    }
    const filtered = allHistoryReservations.filter(r => {
        const date = String(r.check_in_date || "").slice(0, 10);
        return (!from || date >= from) && (!to || date <= to);
    });
    renderHistory(filtered);
    showHistoryMessage(filtered.length ? "" : "No reservations match the selected dates.", false);
}

document.addEventListener("DOMContentLoaded", async () => {
    const filters = document.getElementById("history-filters");
    if (filters) filters.addEventListener("submit", applyHistoryFilters);
    document.getElementById("history-clear")?.addEventListener("click", () => {
        document.getElementById("history-filters").reset();
        applyHistoryFilters();
    });
    const session = getHistoryAuthSession();

    if (!session || !session.customerId) {
        window.location.href = "login.html";
        return;
    }

    try {
        const payload = await fetchReservationHistory(session.customerId);
        const reservations = payload.reservations || [];

        if (reservations.length === 0) {
            allHistoryReservations = [];
            showHistoryMessage("You don't have any past reservations yet.", false);
            return;
        }

        allHistoryReservations = reservations;
        applyHistoryFilters();
    } catch (error) {
        showHistoryMessage(error.message || "Unable to load reservation history at this time.", true);
    }
});
