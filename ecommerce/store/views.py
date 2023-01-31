import json
import datetime

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *
from .utils import cartData, questOrder
from django.shortcuts import render
from django import template

# Create your views here.

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products': products,
        'cartItems': cartItems
        }
    return render(request, 'store/store.html', context)

def cart(request):
    '''This function returns the cart page'''

    data = cartData(request)
    cartItems = data.get('cartItems', 0)
    order = data.get('order', None)
    items = data.get('items', [])

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
        }
    return render(request, 'store/cart.html', context)

def product_view(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'store/product_view.html', {'product': product})

register = template.Library()

@register.filter
def check_product_info(product):
    return all(value for key, value in product.__dict__.items() if not key.startswith('_'))

def checkout(request):
    '''This function returns the checkout page'''

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems
        }

    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body.decode())
    productId = data['productId']
    action = data['action']

    print(f'Action: {action}\nProductId: {productId}')

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        if orderItem.quantity > 0:
            orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item updated', status=200, safe=False)

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = questOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', status=200, safe=False)

"""
**Overview**

The following code is a set of views for an e-commerce store application 
using Django framework. It includes functions for handling requests for 
the store page, cart page, product view page, checkout page and processing 
orders.

**Functionality**

'store' function returns the store page by rendering the store.html template and 
passing product objects and the number of items in the cart as context.

'cart' function returns the cart page by rendering the cart.html template and 
passing order, items, and the number of items in the cart as context.

'product_view' function returns the product view page by rendering the 
product_view.html template and passing a specific product object as context.

'checkout' function returns the checkout page by rendering the checkout.html 
template and passing items, order, and the number of items in the cart as context.

'updateItem' function updates the quantity of an item in the cart through a JSON 
request. It adds or removes a quantity of the specified product based on 
the "action" parameter in the request.

'processOrder' function processes the order by creating or updating the order 
and shipping address objects. If the user is authenticated, the order will 
be associated with the customer. If not, the customer and order objects will 
be created as a "guest order". It returns a JSON response with the message 
"Payment complete!" upon success.

'check_product_info' is a custom filter that checks if all the required 
information of a product object is available.

Note: The views use the cartData and questOrder functions from the utils 
module for retrieving the cart information and creating a guest order 
respectively.

"""