document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('menu-toggle');
    const menu = document.querySelector('.menu');

    menuToggle.addEventListener('change', function () {
        if (this.checked) {
            menu.style.left = '0';
        } else {
            menu.style.left = '-100%';
        }
    });
});
