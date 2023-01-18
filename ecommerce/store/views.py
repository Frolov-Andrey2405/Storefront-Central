from django.shortcuts import render
from .models import *
# Create your views here.

def store(request):
    '''This function retrieves all products in the system and returns them to the store page'''
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)

def cart(request):
    '''This function returns the cart page'''
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        
    context = {'items': items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    '''This function returns the checkout page'''
    context = {}
    return render(request, 'store/checkout.html', context)



