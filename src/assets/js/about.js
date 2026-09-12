/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Wires the about page's "Send an Inquiry" form to the /api/contact endpoint.
*/

"use strict";

const CONTACT_ENDPOINT = `${API_BASE_URL}/api/contact`;

function showContactMessage(text, isError) {
  const messageElement = document.getElementById("contact-message");

  if (!messageElement) {
    return;
  }

  messageElement.textContent = text;
  messageElement.classList.toggle("error", Boolean(isError));
  messageElement.classList.toggle("success", !isError);
}

async function submitContactMessage(name, email, subject, message) {
  const response = await fetch(CONTACT_ENDPOINT, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, subject, message }),
  });

  const data = await response.json().catch(() => ({}));
  return { ok: response.ok, data };
}

function setupContactForm() {
  const form = document.getElementById("contact-form");

  if (!form) {
    return;
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const name = document.getElementById("contactName").value.trim();
    const email = document.getElementById("contactEmail").value.trim();
    const subject = document.getElementById("contactSubject").value.trim();
    const message = document.getElementById("contactMessage").value.trim();

    const submitButton = form.querySelector("button[type=submit]");
    submitButton.disabled = true;
    showContactMessage("Sending your message...", false);

    try {
      const { ok, data } = await submitContactMessage(
        name,
        email,
        subject,
        message,
      );

      if (!ok || !data.success) {
        showContactMessage(data.reason || "Unable to send your message.", true);
        return;
      }

      showContactMessage("Thanks! Your message has been sent.", false);
      form.reset();
    } catch (error) {
      showContactMessage("Unable to reach the server. Please try again.", true);
    } finally {
      submitButton.disabled = false;
    }
  });
}

document.addEventListener("DOMContentLoaded", setupContactForm);
