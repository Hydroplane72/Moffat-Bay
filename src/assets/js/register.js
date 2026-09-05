/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Wires the registration form to the /api/auth/register endpoint and signs the
new guest in immediately, mirroring assets/js/login.js.
*/

"use strict";

const REGISTER_ENDPOINT = `${API_BASE_URL}/api/auth/register`;
const POST_REGISTER_REDIRECT = "reservation.html";

// Requires 8+ characters with at least one uppercase, one lowercase, and one digit
const PASSWORD_PATTERN = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/;

function showRegisterMessage(text, isError) {
    const messageElement = document.getElementById("register-message");

    if (!messageElement) {
        return;
    }

    messageElement.textContent = text;
    messageElement.classList.toggle("error", Boolean(isError));
    messageElement.classList.toggle("success", !isError);
}

async function submitRegistration(payload) {
    const response = await fetch(REGISTER_ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    });

    const data = await response.json().catch(() => ({}));
    return { ok: response.ok, data };
}

function setupRegisterForm() {
    const form = document.getElementById("register-form");

    if (!form) {
        return;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const emailInput = document.getElementById("email");
        const telephoneInput = document.getElementById("telephone");
        const firstNameInput = document.getElementById("firstName");
        const lastNameInput = document.getElementById("lastName");
        const passwordInput = document.getElementById("password");
        const confirmPasswordInput = document.getElementById("confirmPassword");

        const email = emailInput.value.trim();
        const telephone = telephoneInput.value.trim();
        const firstName = firstNameInput.value.trim();
        const lastName = lastNameInput.value.trim();
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;

        if (!isValidEmail(email)) {
            showRegisterMessage("Please enter a valid email address.", true);
            return;
        }

        if (!telephone || !firstName || !lastName) {
            showRegisterMessage("Please fill in all required fields.", true);
            return;
        }

        if (!PASSWORD_PATTERN.test(password)) {
            showRegisterMessage(
                "Password must be at least 8 characters with one uppercase letter, one lowercase letter, and one number.",
                true,
            );
            return;
        }

        if (password !== confirmPassword) {
            showRegisterMessage("Passwords do not match.", true);
            return;
        }

        const submitButton = form.querySelector("button[type=submit]");
        submitButton.disabled = true;
        showRegisterMessage("Creating your account...", false);

        try {
            const { ok, data } = await submitRegistration({
                email,
                phone: telephone,
                first_name: firstName,
                last_name: lastName,
                password,
            });

            if (!ok || !data.success) {
                showRegisterMessage(data.reason || "Unable to create your account.", true);
                return;
            }

            localStorage.setItem(
                "mbl_session",
                JSON.stringify({
                    customerId: data.customer_id,
                    firstName: data.first_name,
                    email,
                }),
            );

            showRegisterMessage("Account created. Redirecting...", false);
            window.location.href = POST_REGISTER_REDIRECT;
        } catch (error) {
            showRegisterMessage("Unable to reach the server. Please try again.", true);
        } finally {
            submitButton.disabled = false;
        }
    });
}

document.addEventListener("DOMContentLoaded", setupRegisterForm);
