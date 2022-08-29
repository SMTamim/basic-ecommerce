page = window.location.href.split("/");
if (page[page.length - 1] === "store") {
    if (document.readyState == "loading") {
        document.addEventListener("DOMContentLoaded", setProduct);
    } else {
        setProduct();
    }
}

async function getProduct() {
    response = await fetch("http://127.0.0.1:5000/api/products", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
        },
        redirect: "follow",
        referrerPolicy: "no-referrer",
        body: JSON.stringify({
            count: 20,
            page: 1,
        }),
    });

    return response.json();
}

function setProduct() {
    const itemContainer = document.querySelector(".item-container");
    getProduct().then((data) => {
        data = data[0].payload;
        for (let i of data) {
            console.log(i);
            itemContainer.innerHTML += `
                <div class="items">
                <span class="item-title">${i.prod_name}</span>
                <img class="item-image" src="static/uploads/${i.prod_img}" alt="">
                <div class="item-details">
                    <span class="item-price">৳ ${i.prod_price}</span>
                    <button class="btn btn-primary item-btn">ADD TO CART</button>
                </div>
            `;
        }
        ready();
    });
}

function ready() {
    var removeButton = document.getElementsByClassName("btn-danger");
    for (var i = 0; i < removeButton.length; i++) {
        removeButton[i].addEventListener("click", removed);
    }

    var itemQuantity = document.getElementsByClassName("cart-quantity-input");
    for (var i = 0; i < itemQuantity.length; i++) {
        itemQuantity[i].addEventListener("change", quantityChanged);
    }

    var addToCart = document.getElementsByClassName("item-btn");
    for (var i = 0; i < addToCart.length; i++) {
        addToCart[i].addEventListener("click", addToCartClicked);
    }

    var purchaseBtn = document.getElementsByClassName("btn-purchase")[0];
    purchaseBtn.addEventListener("click", purchased);
}

function removeAll() {
    var i = 0;
    var rmv = document.getElementsByClassName("btn-danger");
    while (rmv.length != 0) {
        rmv[0].parentElement.parentElement.remove();
    }
    updateCartTotal();
}

function purchased() {
    var totalPrice = parseFloat(
        document.getElementsByClassName("cart-total-price")[0].innerText.replace("৳", "")
    );
    if (totalPrice <= 0) {
        alert("Nothing to purchase!");
    } else {
        alert("Thank You for Purchasing from us!!!");
        removeAll();
    }
}

function removed(event) {
    var buttonClicked = event.target;
    buttonClicked.parentElement.parentElement.remove();
    updateCartTotal();
}

function addToCartClicked(event) {
    var button = event.target;
    button = button.parentElement.parentElement;
    var title = button.getElementsByClassName("item-title")[0].innerText;
    var price = button.getElementsByClassName("item-price")[0].innerText;
    var imgSrc = button.getElementsByClassName("item-image")[0].src;

    var container = document.getElementsByClassName("cart-items-container")[0];
    var cartItems = container.getElementsByClassName("cart-item-title");
    for (var i = 0; i < cartItems.length; i++) {
        if (cartItems[i].innerText == title) {
            alert("Item already in CART!!");
            return;
        }
    }

    var cartRow = document.createElement("div");
    cartRow.classList.add("cart-row");
    cartRow.innerHTML = `
    <div class="cart-item cart-column">
        <img src="${imgSrc}" alt="" class="cart-item-img">
        <span class="cart-item-title">${title}</span>
    </div>
    <span class="cart-column cart-price">${price}</span>
    <div class="cart-column cart-quantity">
        <input class="cart-quantity-input" type="number" name="" id="" value="1">
        <button class="btn btn-danger">REMOVE</button>
    </div>`;
    container.append(cartRow);
    cartRow.getElementsByClassName("btn-danger")[0].addEventListener("click", removed);
    cartRow
        .getElementsByClassName("cart-quantity-input")[0]
        .addEventListener("change", quantityChanged);
    updateCartTotal();
}

function quantityChanged(event) {
    var input = event.target.value;
    if (isNaN(input) || input <= 0) {
        event.target.value = 1;
    }
    updateCartTotal();
}

function updateCartTotal() {
    var cartItems = document.getElementsByClassName("cart-items-container")[0];
    var cartRows = cartItems.getElementsByClassName("cart-row");
    var total = 0;
    for (var i = 0; i < cartRows.length; i++) {
        var price = parseFloat(
            cartRows[i].getElementsByClassName("cart-price")[0].innerText.replace("৳", "")
        );

        var quantity = cartRows[i].getElementsByClassName("cart-quantity-input")[0].value;
        total = total + price * quantity;
    }
    total = Math.round(total * 100) / 100;
    document.getElementsByClassName("cart-total-price")[0].innerText = "৳" + total;
}
