import { findChildNodeDFS } from './domUtils.js';
import { observeMain, waitForMainElement } from './observer.js';
import { addToQueue, processQueue } from './queue.js';

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
    addToQueue({ screen_name, targetID });
    processQueue(10, sendToServer);
}

async function sendToServer(batch) {
    return new Promise((resolve, reject) => {
    //TODO: Replace with real working command
    setTimeout(() => {
        if (Math.random() < 0.9) {
        resolve({ status: "success", data: batch });
        } else {
        reject(new Error("Server error"));
        }
    }, 1000);
    });
}

async function init() {
    console.log("Waiting for <main> element to load...");
    const mainElement = await waitForMainElement();
    console.log("<main> element found. Initializing observer...");
    observeMain(mainElement, handleNewArticle);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
    } else {
    init();
    }