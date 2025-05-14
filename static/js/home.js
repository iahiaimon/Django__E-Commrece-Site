
document.addEventListener("DOMContentLoaded", () => {
    const items = document.querySelectorAll("[data-carousel-item]");
    const prevBtn = document.querySelector("[data-carousel-prev]");
    const nextBtn = document.querySelector("[data-carousel-next]");
    const indicators = document.querySelectorAll("[data-carousel-slide-to]");
    let current = 0;

    function showSlide(index) {
        items.forEach((item, i) => {
            item.classList.toggle("hidden", i !== index);
            item.classList.toggle("block", i === index);
        });
        indicators.forEach((indicator, i) => {
        indicator.setAttribute("aria-current", i === index ? "true" : "false");
        });
    }

    prevBtn.addEventListener("click", () => {
        current = (current - 1 + items.length) % items.length;
    showSlide(current);
    });

    nextBtn.addEventListener("click", () => {
        current = (current + 1) % items.length;
    showSlide(current);
    });

    indicators.forEach((button, index) => {
        button.addEventListener("click", () => {
            current = index;
            showSlide(current);
        });
    });

    // Initialize
    showSlide(current);
});