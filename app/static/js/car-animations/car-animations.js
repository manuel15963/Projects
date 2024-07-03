document.addEventListener('DOMContentLoaded', function() {
    const carouselContainer = document.querySelector('.carousel-container');
    const products = document.querySelectorAll('.product-item');
    const productWidth = products[0].offsetWidth;
    let scrollAmount = 0;

    // Clone the first few products to create a looping effect
    for (let i = 0; i < products.length; i++) {
        const clone = products[i].cloneNode(true);
        carouselContainer.appendChild(clone);
    }

    function autoScroll() {
        scrollAmount += 1;
        if (scrollAmount >= carouselContainer.scrollWidth / 2) {
            scrollAmount = 0;
        }
        carouselContainer.style.transform = `translateX(-${scrollAmount}px)`;
    }

    setInterval(autoScroll, 50);
});
