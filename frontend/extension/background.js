chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "sendPin") {
        console.log("🌍 Forwarding PIN to Next.js API:", message.pin);

        fetch("http://localhost:3000/api/sendPins", {
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pin: message.pin })
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Response from Next.js API:", data);
            sendResponse(data);
        })
        .catch(error => {
            console.error("❌ Error forwarding PIN:", error);
            sendResponse({ success: false, error: error.message });
        });

        return true; // Allows sendResponse to work asynchronously
    }

    else if (message.action === "resizePopup" && message.height) {
        console.log(`📏 Resizing popup to ${message.height}px`);
        chrome.windows.getCurrent((win) => {
            chrome.windows.update(win.id, { height: message.height });
        });
    }
});
