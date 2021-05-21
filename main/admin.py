from django.contrib import admin
from .models import User, Product, Cart, Order, StoreSecret, WarehouseSecret

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(StoreSecret)
admin.site.register(WarehouseSecret)

