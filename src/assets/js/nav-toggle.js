/*
Description:
Shared responsive navigation menu toggle used across all Moffat Bay Lodge pages.
*/

"use strict";

function setupMobileNavigation() {
    const menuToggle = document.getElementById("menu-toggle");
    const mainNav = document.getElementById("main-nav");

    if (!menuToggle || !mainNav) {
        return;
    }

    if (!mainNav.id) {
        mainNav.id = "main-nav";
    }

    menuToggle.setAttribute("aria-controls", mainNav.id);
    menuToggle.setAttribute("aria-expanded", "false");

    function closeMenu() {
        mainNav.classList.remove("open");
        menuToggle.setAttribute("aria-expanded", "false");
    }

    menuToggle.addEventListener("click", () => {
        const isOpen = mainNav.classList.toggle("open");
        menuToggle.setAttribute("aria-expanded", String(isOpen));
    });

    mainNav.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", closeMenu);
    });

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && mainNav.classList.contains("open")) {
            closeMenu();
            menuToggle.focus();
        }
    });

    window.addEventListener("resize", () => {
        if (window.innerWidth > 1040) {
            closeMenu();
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    setupMobileNavigation();
});
