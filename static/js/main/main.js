// Theme Functions
function toggleTheme() {
  const currentTheme =
    document.documentElement.getAttribute("data-theme") || "light";

  const newTheme = currentTheme === "light" ? "dark" : "light";

  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  updateThemeIcon(newTheme);

  showToast(`Switched to ${newTheme} theme`, 'info');
}

function updateThemeIcon(theme) {
  const themeToggle = document.getElementById("themeToggle");
  if (themeToggle) {
    themeToggle.innerHTML =
      theme === "light"
        ? '<i class="fas fa-moon"></i>'
        : '<i class="fas fa-sun"></i>';
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const themeToggle = document.getElementById("themeToggle");

  if (themeToggle) {
    themeToggle.addEventListener("click", toggleTheme);
  }

  const savedTheme = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", savedTheme);
  updateThemeIcon(savedTheme);
});

// Toast Notification System
function showToast(message, type = 'info') {
  // Remove existing toasts
  const existingToasts = document.querySelectorAll('.toast');
  existingToasts.forEach(toast => toast.remove());
  
  // Create new toast
  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);
  
  // Show toast
  setTimeout(() => toast.classList.add('show'), 10);
  
  // Hide after 3 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

document.addEventListener("DOMContentLoaded", function () {
    const toggle = document.querySelector(".filter-toggle");
    const collapsible = document.querySelector(".collapsible");

    toggle.addEventListener("click", function () {
        collapsible.classList.toggle("active");
    });
});



function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');

    for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;
};

document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".add-to-cart").forEach(button => {

        button.addEventListener("click", function () {

            const productId = this.dataset.productId;
            const btn = this;
            const count = document.querySelector(".cart-count").innerHTML;

            // Find closest product card (safe)
            const productCard = this.closest(".product-card") || document;

            // Try to find quantity input
            const quantityInput = productCard.querySelector(".qty-input");

            // Default quantity
            let quantity = 1;

            if (quantityInput) {
                quantity = parseInt(quantityInput.value) || 1;
            }

            fetch('/api/cart/', {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken()
                },
                body: JSON.stringify({
                    product_id: productId,
                    quantity: quantity
                })
            })
            .then(res => res.json())
            .then(data => {
                if (data.status === "Added") {
                    document.querySelector(".cart-count").innerText = data.cart_count;

                    btn.textContent = "Added";
                    btn.classList.remove("btn-primary");
                    btn.classList.add("btn-success");
                    showToast("Added to Cart", "success");

                } else if (data.status === "Removed") {
                    document.querySelector(".cart-count").innerText = data.cart_count;

                    btn.textContent = "Add to Cart";
                    btn.classList.remove("btn-success");
                    btn.classList.add("btn-primary");
                    showToast("Removed from Cart");
                }

                else {
                    showToast("Something went wrong", "error");
                }

            })
            .catch(error => {
                console.error("Fetch Error:", error);
                showToast("Network error", "error");
            });

        });

    });

});








