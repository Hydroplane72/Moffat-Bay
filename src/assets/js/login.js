/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Wires the login form to the /api/auth/login endpoint and stores the resulting
session so the shared auth-chip and other pages know a guest is signed in.
*/

"use strict";

const LOGIN_ENDPOINT = `${API_BASE_URL}/api/auth/login`;
const POST_LOGIN_REDIRECT = "reservation.html";

function showLoginMessage(text, isError) {
  const messageElement = document.getElementById("login-message");

  if (!messageElement) {
    return;
  }

  messageElement.textContent = text;
  messageElement.classList.toggle("error", Boolean(isError));
  messageElement.classList.toggle("success", !isError);
}

async function submitLogin(email, password) {
  const response = await fetch(LOGIN_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  const data = await response.json().catch(() => ({}));
  return { ok: response.ok, data };
}

function setupLoginForm() {
  const form = document.getElementById("login-form");

  if (!form) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const emailInput = document.getElementById("email");
    const passwordInput = document.getElementById("password");
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!isValidEmail(email)) {
      showLoginMessage("Please enter a valid email address.", true);
      return;
    }

    if (!password) {
      showLoginMessage("Please enter your password.", true);
      return;
    }

    const submitButton = form.querySelector("button[type=submit]");
    submitButton.disabled = true;
    showLoginMessage("Signing in...", false);

    try {
      const { ok, data } = await submitLogin(email, password);

      if (!ok || !data.success) {
        showLoginMessage(data.reason || "Invalid email or password.", true);
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

      showLoginMessage("Login successful. Redirecting...", false);
      window.location.href = POST_LOGIN_REDIRECT;
    } catch (error) {
      showLoginMessage("Unable to reach the server. Please try again.", true);
    } finally {
      submitButton.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", setupLoginForm);
