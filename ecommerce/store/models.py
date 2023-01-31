from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Customer(models.Model):
    '''This class represents a customer in the system'''
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    '''This class represents a product in the system'''
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=False)
    image_url = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True, null=True, blank=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    sku = models.CharField(max_length=200, null=True, blank=True)
    width = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    depth = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    warranty = models.TextField(null=True, blank=True)
    shipping_fees = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    estimated_delivery_time = models.CharField(max_length=200, null=True, blank=True)
    return_policy = models.TextField(null=True, blank=True)
    step_by_step_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    '''This class represents an order in the system'''
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()

        for i in orderitems:
            if i.product.digital == False:
                shipping = True

        return shipping

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    '''This class represents an item in an order in the system'''
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    '''This class represents a shipping address for an order in the system'''
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

"""
**Overview**

This file contains four classes: Customer, Product, Order, OrderItem and 
ShippingAddress. These classes represent different entities in an e-commerce 
system and their relationships with each other.

**Functionality**

- Customer
The Customer class represents a customer in the system. It has fields for the 
customer's name, email, and a OneToOne relationship with Django's built-in 
User model.

- Product
The Product class represents a product in the system. It has fields for 
product details such as name, price, image URL, description, availability, 
rating, category, brand, SKU, dimensions, weight, warranty, shipping fees, 
estimated delivery time, return policy, and a step-by-step description.

- Order
The Order class represents an order in the system. It has fields for the 
customer who made the order, the date the order was placed, the completion 
status of the order, and the transaction ID. It also has properties to return 
the shipping status, the total amount of the order, and the number of items in 
the order.

- OrderItem
The OrderItem class represents an item in an order in the system. It has 
fields for the product, the order it belongs to, the quantity of the product, 
and the date it was added to the order. It has a property to return the total 
amount for this item.

- ShippingAddress
The ShippingAddress class represents a shipping address for an order in 
the system. It has fields for the customer, address, city, state, zip code, 
and a date added field.
"""