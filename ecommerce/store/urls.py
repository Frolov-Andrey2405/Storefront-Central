from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('view/<int:id>/', views.product_view, name='product_view'),
	path('checkout/', views.checkout, name="checkout"),
	path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]

"""
**Overview**

This file contains the URL patterns for the e-commerce store web application. 
The URLs are defined using the path function from django.urls and map to views 
in the views.py file.

**Functionality**

The urlpatterns list defines the URLs for the following pages in 
the e-commerce store:

- '/' - The store page, which displays the list of products available 
for purchase.
- '/cart/' - The cart page, which displays the items the user has added 
to their shopping cart.
- '/view/<int:id>/' - The product view page, which displays details about 
a specific product.
- '/checkout/' - The checkout page, which allows the user to purchase 
the items in their cart.
- '/update_item/' - The update item page, which updates the quantity of 
an item in the user's cart.
- '/process_order/' - The process order page, which processes the order 
made by the user.

"""