const queue = [];
const screenNameSet = new Set();

function findChildNodeDFS(element, selector) {
    if (element.matches(selector)) {
    return element;
    }

    for (const child of element.children) {
    const result = findChildNodeDFS(child, selector);
    if (result) {
        return result;
    }
    }

    return null;
    }

    function handleNewArticle(article) {

    const targetItem = findChildNodeDFS(article, 'a');
    if (!targetItem) {
    console.log("No <a> element found in the article.");
    return;
    }

    const targetIDElement = findChildNodeDFS(article, '[data-testid="User-Name"]');
    const targetID = targetIDElement ? targetIDElement.getAttribute("id") : null;
    if (!targetID) {
    console.log("No element with data-testid='User-Name' found in the article.");
    return;
    }

    const screen_name = targetItem.getAttribute('href').slice(1);

    if (screenNameSet.has(screen_name)) {
    console.log("Duplicate screen_name found. Not adding to queue:", screen_name);
    return;
    }

    queue.push({ screen_name, targetID });
    screenNameSet.add(screen_name);
    console.log("Added to queue:", { screen_name, targetID });
    console.log("Queue:", queue);
}

function observeMain(mainElement) {
    const observer = new MutationObserver((mutationsList) => {
    for (const mutation of mutationsList) {
        if (mutation.type === "childList") {
        mutation.addedNodes.forEach((node) => {
            if (node.nodeType === Node.ELEMENT_NODE) {
            if (node.tagName.toLowerCase() === "article") {
                handleNewArticle(node);
            } else {
                const articles = node.querySelectorAll("article");
                articles.forEach((article) => handleNewArticle(article));
            }
            }
        });
        }
    }
    });

    observer.observe(mainElement, { childList: true, subtree: true });
    console.log("Observing <main> for new articles...");
    }

function waitForMainElement() {
    return new Promise((resolve) => {
    const observer = new MutationObserver((mutationsList, obs) => {
        const mainElement = document.querySelector('main');
        if (mainElement) {
        obs.disconnect();
        resolve(mainElement);
        }
    });

    observer.observe(document.body, { childList: true, subtree: true });
    });
}

async function init() {
    console.log("Waiting for <main> element to load...");
    const mainElement = await waitForMainElement();
    console.log("<main> element found. Initializing observer...");
    observeMain(mainElement);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
    } else {
    init();
}

function processQueue() {
    while (queue.length > 0) {
    const item = queue.shift(); // Remove the first item from the queue
    console.log("Processing item:", item);

    // Perform your desired action with the item
    // Example: Send data to a server
    // fetch('/api/save', { method: 'POST', body: JSON.stringify(item) });
    }
}

setInterval(processQueue, 5000);