function selectShipping(ShippingId) {
    const OrderId = document.getElementById('order_id').value;

    fetch('/api/update-shipping/',{
        method : "POST",
        headers:{
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            order_id: OrderId,
            shipping_id : ShippingId
        })

    })
    .then(res=>res.json())
    .then(data => {
        const type = document.getElementById('shipping_type').innerHTML = data.shipping_type.toUpperCase();
        document.getElementById('shipping_price').innerHTML = `$${data.shipping_price}`;
        document.getElementById('total_amount').innerHTML = `$${data.total_amount}`;
        showToast(`Shipping Type Changed to ${type}`, "success");
    });
}

function selectAddress(AddressId) {
    const OrderId = document.getElementById('order_id').value;

    fetch('/api/update-order-address/',{

        method : "POST",
        headers :{
           "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body : JSON.stringify({
            order_id : OrderId,
            address_id : AddressId
        })
    })
    .then(res => res.json())
    .then(data => {
        showToast(`Address Changed to ${data.type}`,"success")
    });

}

function updateCartQuantity(cartId) {
    const quantity = parseInt(document.getElementById(`cartQnt-${cartId}`).value);

    fetch('/api/update-cart-quantity/',{
        method : "POST" ,
        headers: {
            "X-CSRFToken": getCSRFToken(),
            "Content-Type": "application/json",
        },
        body : JSON.stringify({'cart_id':cartId , 'quantity': quantity})
    })
    .then(res=>res.json())
    .then(data => {
        const span = document.getElementById('cartTotal')
        span.innerText = `${data.new_total}`
        showToast(`Sucessfully updated quantity of ${data.product_name}`, "success");
    });
}
