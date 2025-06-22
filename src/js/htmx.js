import htmx from "htmx.org";
window.htmx = htmx;

document.addEventListener('DOMContentLoaded', () => {
    // Re-initialize htmx if needed
    htmx.process(document.body);
});
