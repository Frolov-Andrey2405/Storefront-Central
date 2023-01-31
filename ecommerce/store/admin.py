from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

"""
**Overview**

The code provides the administration for Django models, which is a way to 
interact with the data stored in the database.

**Functionality**

The code imports the necessary modules to register the models in the Django 
administration site. The models are Customer, Product, Order, OrderItem, and 
ShippingAddress. The 'admin.site.register' function is used to register each 
model, which allows the administrator to view, add, edit, and delete instances 
of each model in the Django administration site.

"""