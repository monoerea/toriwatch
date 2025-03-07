export function findChildNodeDFS(element, selector) {
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