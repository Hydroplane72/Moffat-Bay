/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Populates the shared header auth-chip on every page based on the locally
stored login session, and handles logging out.
*/

"use strict";

const AUTH_SESSION_KEY = "mbl_session";

function getAuthSession() {
  try {
    const raw = localStorage.getItem(AUTH_SESSION_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (error) {
    return null;
  }
}

function clearAuthSession() {
  localStorage.removeItem(AUTH_SESSION_KEY);
}

function renderAuthChip() {
  const chip = document.getElementById("auth-chip");

  if (!chip) {
    return;
  }

  const session = getAuthSession();
  chip.textContent = "";

  if (session && session.firstName) {
    const greeting = document.createElement("span");
    greeting.className = "auth-chip-greeting";
    greeting.textContent = `Welcome, ${session.firstName}`;

    const logoutButton = document.createElement("button");
    logoutButton.type = "button";
    logoutButton.className = "btn btn-ghost";
    logoutButton.textContent = "Logout";
    logoutButton.addEventListener("click", () => {
      clearAuthSession();
      window.location.href = "index.html";
    });

    chip.append(greeting, logoutButton);
    return;
  }

  const loginLink = document.createElement("a");
  loginLink.className = "btn btn-ghost";
  loginLink.href = "login.html";
  loginLink.textContent = "Login";

  const registerLink = document.createElement("a");
  registerLink.className = "btn btn-primary";
  registerLink.href = "register.html";
  registerLink.textContent = "Register";

  chip.append(loginLink, registerLink);
}

document.addEventListener("DOMContentLoaded", renderAuthChip);
