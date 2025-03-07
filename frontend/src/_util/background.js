chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (!tab.url) return;

    const handleTwitterUrl = (url, path, paramKey) => {
        if (url.includes(path)) {
            const queryParameters = new URLSearchParams(url.split("?")[1] || "");
            chrome.tabs.sendMessage(tabId, {
                type: "NEW",
                timeline: queryParameters.get(paramKey) || path
            });
        }
    };

    if (tab.url.includes("twitter.com/home")) {
        handleTwitterUrl(tab.url, "twitter.com/home", "home");
    } else if (tab.url.includes("twitter.com/") && tab.url.includes("/status/")) {
        handleTwitterUrl(tab.url, "twitter.com/", "status");
    } else if (tab.url.includes("twitter.com/")) {
        handleTwitterUrl(tab.url, "twitter.com/", "/");
    }
});