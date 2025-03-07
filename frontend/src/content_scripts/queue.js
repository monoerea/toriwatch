const queue = [];
const screenNameSet = new Set();

export function addToQueue(item) {
    if (!screenNameSet.has(item.screen_name)) {
    queue.push(item);
    screenNameSet.add(item.screen_name);
    console.log("Added to queue:", item);
    } else {
    console.log("Duplicate screen_name found. Not adding to queue:", item.screen_name);
    }
    }

export function processQueue(batchSize, sendToServer) {
    if (queue.length === 0) {
    console.log("Queue is empty. Nothing to process.");
    return;
    }

    const batch = queue.splice(0, batchSize);
    console.log("Processing batch:", batch);

    sendToServer(batch)
    .then((response) => {
        console.log("Server response:", response);
        if (queue.length > 0) {
        processQueue(batchSize, sendToServer);
        }
    })
    .catch((error) => {
        console.error("Error sending batch to server:", error);
        queue.unshift(...batch); // Re-add the batch to the queue
        console.log("Re-added batch to queue:", batch);
    });
    }