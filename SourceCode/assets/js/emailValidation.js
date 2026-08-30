/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
Reusable input validation helpers. Each validator is a standalone function so
additional checks (beyond email) can be added here without touching existing ones.
*/

// Matches "text@domain.tld" - requires a "." between the domain and a letters-only extension
const EMAIL_PATTERN = /^[^\s@]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

function isValidEmail(email) {
    return EMAIL_PATTERN.test(email.trim());
}

// Validates an email input; when showMessage is true, adds/removes a single validation message beneath it
function checkEmailInput(inputElement, showMessage) {
    const valid = isValidEmail(inputElement.value);
    const messageId = inputElement.id + "-validation-message";
    let messageElement = document.getElementById(messageId);

    if (valid) {
        if (messageElement) {
            messageElement.remove();
        }
        return true;
    }

    if (showMessage) {
        if (!messageElement) {
            messageElement = document.createElement("p");
            messageElement.id = messageId;
            messageElement.className = "input-validation-message";
            inputElement.insertAdjacentElement("afterend", messageElement);
        }
        messageElement.textContent = "Please enter a valid email address.";
    }

    return false;
}
