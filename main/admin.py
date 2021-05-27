from django.contrib import admin
from .models import User, Product, Cart, Order, StoreSecret, WarehouseSecret, TrackingNumber, ReportDue

class UserAdmin(admin.ModelAdmin):
	list_display = ('username', 'store_name', 'store_location', 'allow_edit', 'is_superuser')

class ProductAdmin(admin.ModelAdmin):
	list_display = ('sap', 'category', 'description', 'unit')

class OrderAdmin(admin.ModelAdmin):
	list_display = ('user', 'date', 'checkout', 'confirm', 'confirmation_number')

class TrackingAdmin(admin.ModelAdmin):
	list_display = ('order', 'tracking_number')

class CartAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'quantity', 'shipped_quantity')

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(TrackingNumber, TrackingAdmin)
admin.site.register(StoreSecret)
admin.site.register(WarehouseSecret)
admin.site.register(ReportDue)
