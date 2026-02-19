function cancelOrder(OrderId) {
    fetch('/api/cancel-order/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ order_id: OrderId })
    })
    .then(res => res.json())
    .then(data => {
        // Update status
        const statusElem = document.getElementById(`status-${OrderId}`);
        if (statusElem) statusElem.innerText = "CANCELLED";

        // Replace buttons
        const footer = document.querySelector(`#order-${OrderId} .order-actions`);
        if (footer) {
            footer.innerHTML = `
                <button class="btn btn-outline"
                    onclick="window.location.href='/checkout/${OrderId}/'">
                    <i class="fas fa-redo"></i> Order Again
                </button>
                <button class="btn btn-outline"
                    onclick="deleteOrder('${OrderId}')">
                    <i class="fa fa-trash"></i> Delete
                </button>
            `;
        }

        showToast(data.message || "Order cancelled successfully", "success");
    })
    .catch(err => {
        console.error(err);
        showToast("Something went wrong!", "error");
    });
}


function deleteOrder(OrderId) {

    fetch('/api/delete-order/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ order_id: OrderId })
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Request failed");
        }
        return res.json();
    })
    .then(data => {
        // Remove entire order block
        const orderItem = document.getElementById(`order-${OrderId}`);
        if (orderItem) orderItem.remove();

        showToast(data.message || "Order deleted successfully", "success");
    })
    .catch(err => {
        console.error("Delete failed:", err);
        showToast("Something went wrong!", "error");
    });
}

