
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


// Cart functionality


document.addEventListener("DOMContentLoaded", () => {
    const cart = JSON.parse(localStorage.getItem("cart")) || [];

    function saveCart() {
        localStorage.setItem("cart", JSON.stringify(cart));
    }

    function addToCart(product) {
        const existing = cart.find(item => item.id === product.id);
    if (existing) {
        existing.quantity += 1;
        } else {
        product.quantity = 1;
    cart.push(product);
        }
    saveCart();
    alert(`${product.name} added to cart!`);
    }

    document.querySelectorAll(".add-to-cart").forEach(button => {
        button.addEventListener("click", () => {
            const product = {
                id: button.getAttribute("data-product-id"),
                name: button.getAttribute("data-product-name"),
                price: parseFloat(button.getAttribute("data-product-price")),
            };
            addToCart(product);
        });
    });
});
