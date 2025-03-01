
export function observeMain(mainElement, handleNewArticle) {
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

export function waitForMainElement() {
  return new Promise((resolve) => {
    const observer = new MutationObserver((mutationsList, obs) => {
      const mainElement = document.querySelector('main');
      if (mainElement) {
        obs.disconnect(); // Stop observing
        resolve(mainElement);
      }
    });

    observer.observe(document.body, { childList: true, subtree: true });
  });
}