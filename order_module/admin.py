from django.contrib import admin
from order_module import models

# Register your models here.

admin.site.register(models.Order)
admin.site.register(models.OrderItems)