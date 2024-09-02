// assets/hover.js
document.addEventListener('DOMContentLoaded', function() {
    const divs = document.querySelectorAll('div');
    divs.forEach(div => {
        if (div.id) {
            div.setAttribute('title', div.id);
        }
    });
});