function updateProfileShipping(selected,shippingId) {

    fetch('/api/update-profile-shipping/', {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ shipping_id: shippingId })
    })
    .then(res => res.json())
    .then(data => {
        document.querySelectorAll('.payment-card')
        .forEach(card => card.classList.remove('active'));
        const card = selected.closest('.payment-card');
        card.classList.add('active');
        selected.remove();
        showToast(`Successfully updated Shipping Method to ${data.type}`, 'success');
    })
    .catch(err => {
        console.error("Shipping update failed:", err);
        showToast("Something went wrong!", "error");
    });
}



function updateProfileAddress(selectBtn,addressId) {
   fetch('/api/update-profile-address/',{
    method: "POST",
    headers: {
        "X-CSRFToken": getCSRFToken(),
        "Content-Type": "application/json",
    },
    body: JSON.stringify({address_id: addressId})
   })
   .then(res => res.json())
   .then(data =>{
    
    const oldDefault = document.querySelector('.address-actions:not(:has(button))');    
    if (oldDefault && oldDefault !== selectBtn.parentElement) {
        const oldBtn = document.createElement('button');
        oldBtn.className = "btn btn-outline";
        oldBtn.innerHTML = "Set as Default";

        const card = oldDefault.closest(".address-card");
        id = card.getAttribute("data-id");

        oldBtn.onclick = () => updateProfileAddress(oldBtn,id)
        oldDefault.appendChild(oldBtn);
    }
    selectBtn.remove()
    showToast(`Successfully Set Address to ${data.address}`);
   })
   .catch(err => {
        console.error("Shipping update failed:", err);
        showToast("Something went wrong!", "error");
    });
}