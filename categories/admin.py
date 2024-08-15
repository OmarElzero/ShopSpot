from django.contrib import admin
from categories.models import Category,Product,CartItem,Cart,Order,OrderItem
# Register your models here.
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)