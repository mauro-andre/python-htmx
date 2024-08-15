document.addEventListener("click", function (evt) {
    if (evt.target.matches(".fa-xmark")) {
        const alertElement = document.querySelector("#alert");
        alertElement.innerHTML = "";
        alertElement.className = "";
    }
});

document.addEventListener("htmx:afterOnLoad", function (evt) {
    const newPageTitle = evt.detail.xhr.getResponseHeader("X-Page-Title");
    if (newPageTitle) {
        document.title = newPageTitle;
    }
});

document.addEventListener("htmx:beforeSwap", function (evt) {
    if (evt.detail.xhr.status >= 400 && evt.detail.xhr.status < 500) {
        if (evt.detail.xhr.getResponseHeader("X-Should-Swap")) {
            evt.detail.shouldSwap = true
        }
    }
});
