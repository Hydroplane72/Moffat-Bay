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
    messageEl.className = `message ${isError ? "error" : "success"}`;
}

async function fetchReservationHistory(customerId) {
    const response = await fetch(`${API_BASE_URL}/api/reservations/history?customer_id=${customerId}`);
    return response.json();
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

document.addEventListener("DOMContentLoaded", async () => {
    const session = getHistoryAuthSession();

    if (!session || !session.customerId) {
        window.location.href = "login.html";
        return;
    }

    try {
        const payload = await fetchReservationHistory(session.customerId);
        const reservations = payload.reservations || [];

        if (reservations.length === 0) {
            showHistoryMessage("You don't have any past reservations yet.", false);
            return;
        }

        renderHistory(reservations);
    } catch (error) {
        showHistoryMessage("Unable to load reservation history at this time.", true);
    }
});
