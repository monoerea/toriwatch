document.addEventListener("DOMContentLoaded", () => {
    const iframe = document.getElementById("popupFrame");

    if (!iframe) {
        console.error("🚨 iframe not found.");
        return;
    }

    console.log("✅ popup.js loaded, waiting for messages...");

    window.addEventListener("message", (event) => {
        console.log("📩 Message received:", event.data);

        if (event.origin !== "http://localhost:3000") {
            console.warn("⚠️ Ignoring message from unknown origin:", event.origin);
            return;
        }

        const { height } = event.data;
        if (height && height > 50) {
            console.log(`📏 Resizing popup to ${height}px`);

            iframe.style.height = `${height}px`;

            chrome.runtime.sendMessage({ action: "resizePopup", height });
        } else {
            console.warn("⚠️ Received height is undefined or too small.");
        }
    });
    iframe.style.transition = "height 0.3s ease-in-out";
});

