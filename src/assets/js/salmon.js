/*
Team Name: Red Team
Members:
 - Brayan Covarrubias
 - Matthew Rozendaal
 - Rashai Robertson
 - Tiffany Davidson
Description:
This script controls the playful Index-page salmon interaction.
*/

"use strict";

(function setupSalmonFriend() {
    const salmonElement = document.getElementById("salmon-friend");
    const splashElement = document.getElementById("salmon-splash");

    if (!salmonElement) {
        return;
    }

    const restingInset = 24;
    const proximityDistance = 100;
    const returnDelay = 5000;
    const cursorHoldDuration = 1000;
    let returnTimer;
    let cursorHoldTimer;
    let cursorIsHeld = false;
    let lastPointerPosition = { x: 0, y: 0 };
    let currentPosition = { left: 0, top: 0 };
    let restingPosition = { left: 0, top: 0 };

    function getSalmonSize() {
        return {
            width: salmonElement.getBoundingClientRect().width,
            height: salmonElement.getBoundingClientRect().height
        };
    }

    function clampPosition(left, top) {
        const { width, height } = getSalmonSize();

        return {
            left: Math.min(Math.max(0, left), Math.max(0, window.innerWidth - width)),
            top: Math.min(Math.max(0, top), Math.max(0, window.innerHeight - height))
        };
    }

    function setPosition(position) {
        const safePosition = clampPosition(position.left, position.top);

        currentPosition = safePosition;
        salmonElement.style.left = `${safePosition.left}px`;
        salmonElement.style.top = `${safePosition.top}px`;
    }

    function calculateRestingPosition() {
        const { width, height } = getSalmonSize();

        restingPosition = clampPosition(
            window.innerWidth - width - restingInset,
            window.innerHeight - height - restingInset
        );
    }

    function scheduleReturnHome() {
        window.clearTimeout(returnTimer);
        returnTimer = window.setTimeout(() => {
            calculateRestingPosition();
            setPosition(restingPosition);
        }, returnDelay);
    }

    function jumpToRandomPosition() {
        const { width, height } = getSalmonSize();
        const maxLeft = Math.max(0, window.innerWidth - width);
        const maxTop = Math.max(0, window.innerHeight - height);
        let nextPosition;

        do {
            nextPosition = {
                left: Math.random() * maxLeft,
                top: Math.random() * maxTop
            };
        } while (
            maxLeft > 1 &&
            maxTop > 1 &&
            Math.abs(nextPosition.left - currentPosition.left) < 1 &&
            Math.abs(nextPosition.top - currentPosition.top) < 1
        );

        if (splashElement) {
            const salmonBounds = salmonElement.getBoundingClientRect();

            splashElement.style.left = `${salmonBounds.left + salmonBounds.width / 2}px`;
            splashElement.style.top = `${salmonBounds.top + salmonBounds.height * 0.75}px`;
            splashElement.classList.remove("is-active");
            void splashElement.offsetWidth;
            splashElement.classList.add("is-active");
        }

        cursorIsHeld = true;
        document.body.classList.add("salmon-cursor-near");
        window.clearTimeout(cursorHoldTimer);
        cursorHoldTimer = window.setTimeout(() => {
            cursorIsHeld = false;
            updateCursorProximity({
                clientX: lastPointerPosition.x,
                clientY: lastPointerPosition.y
            });
        }, cursorHoldDuration);

        setPosition(nextPosition);
        scheduleReturnHome();
    }

    function updateCursorProximity(event) {
        lastPointerPosition = {
            x: event.clientX,
            y: event.clientY
        };

        if (cursorIsHeld) {
            return;
        }

        const bounds = salmonElement.getBoundingClientRect();
        const nearestX = Math.max(bounds.left, Math.min(event.clientX, bounds.right));
        const nearestY = Math.max(bounds.top, Math.min(event.clientY, bounds.bottom));
        const distance = Math.hypot(event.clientX - nearestX, event.clientY - nearestY);

        document.body.classList.toggle("salmon-cursor-near", distance <= proximityDistance);
    }

    function handleSalmonEnter(event) {
        updateCursorProximity(event);
        jumpToRandomPosition();
    }

    function handleResize() {
        calculateRestingPosition();
        setPosition(currentPosition);
        scheduleReturnHome();
    }

    function initialize() {
        salmonElement.addEventListener("pointerenter", handleSalmonEnter);
        salmonElement.addEventListener("pointermove", updateCursorProximity);
        window.addEventListener("pointermove", updateCursorProximity, { passive: true });
        window.addEventListener("resize", handleResize);

        calculateRestingPosition();
        setPosition(restingPosition);
        scheduleReturnHome();
    }

    if (salmonElement.complete) {
        initialize();
    } else {
        salmonElement.addEventListener("load", initialize, { once: true });
    }
})();
