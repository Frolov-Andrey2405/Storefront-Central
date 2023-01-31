import json

from .models import *

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}

    print(f'Cart: {cart}')

    items = []
    order = {
        'get_cart_total': 0,
        'get_cart_items': 0,
        'shipping': False
    }

    for i in cart:
        try:
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'image_url': product.image_url,
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)

            if product.digital == False:
                order['shipping'] = True

        except:
            pass
    return {
        'cartItems': order['get_cart_items'],
        'order': order,
        'items': items,
    }

def cartData(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData.get('cartItems', 0)
        order = cookieData.get('order', None)
        items = cookieData.get('items', [])

    return {
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }

def questOrder(request, data):
    
    print('User in not logging in ...')

    print(f'COOKIES: {request.COOKIES}')
    name = data['form']['name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        email = email
    )
    customer.name = name
    customer.save()

    order = Order.objects.create(
        customer = customer,
        complete = False
        )

    for item in items:
        product = Product.objects.get(id=item['product']['id'])
        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    
    return customer, order

"""
**Overview**

This code provides the functionalities of a shopping cart in 
an e-commerce website. It implements the functionalities of adding items 
to the cart, retrieving the items in the cart and creating an order for 
the items in the cart.

**Functionality**

'cookieCart(request)': This function retrieves the items in the cart from 
the cookies and returns a dictionary containing the total number of items, 
the total cost of the items, the items in the cart, and a boolean indicating 
if shipping is required.

'cartData(request)': This function retrieves the items in the cart from either 
the authenticated user's order or from the cookies if the user is 
not authenticated. It returns a dictionary containing the total number of 
items, the total cost of the items, and the items in the cart.

'questOrder(request, data)': This function creates an order for the items in 
the cart for a guest user. It receives the user's name and email from 
the data argument, retrieves the items in the cart from the cookies, 
creates a customer record with the email and name, creates an order for 
the items, and returns the customer and order information.

"""