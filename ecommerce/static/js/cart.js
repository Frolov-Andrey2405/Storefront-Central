var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)

        console.log('USER:', user)
        if (user === 'AnonymousUser') {
            addCookieItem(productId, action)
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function addCookieItem(productId, action) {
    console.log('Not logged in ...')

    if (action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = { 'quantity': 1 }
        } else {
            cart[productId]['quantity'] += 1
        }
    }

    if (action == 'remove') {
        cart[productId]['quantity'] -= 1

        if (cart[productId]['quantity'] <= 0) {
            console.log('Remove Item')
            delete cart[productId]
        }
    }

    console.log('Cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()

}

function updateUserOrder(productId, action) {
    var url = window.location.origin + '/update_item/'
    console.log('URL:', url)

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({
            'productId': productId,
            'action': action
        })
    })

        .then((response) => {
            return response.json();
        })

        .then((data) => {
            console.log('data:', data)
            location.reload()
        });
}

/*

*Overview*

This is a JavaScript code that implements the functionality of updating 
an item in a shopping cart. It consists of two functions, "addCookieItem" 
and "updateUserOrder", that are called based on the status of the user, 
i.e., either anonymous or logged-in.

*Functionality*

- The code starts by retrieving all elements with the class name "update-cart" and 
adding an event listener to each of them to listen for a click event.

- When a click event is triggered, the function retrieves the values of two 
data attributes, "product" and "action", that are attached to the clicked element.

- If the user is an anonymous user, the "addCookieItem" function is called, 
and the product is added or removed from the cart stored in cookies.

- If the user is a logged-in user, the "updateUserOrder" function is called, 
and a POST request is sent to the server to update the order. 
The request contains the productId and action values as a JSON object.

- The server returns the updated information, and the page is reloaded 
to reflect the changes made to the shopping cart.

*/