from django.contrib import admin

from commercial.models import Product, Cart, CartItem, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "score")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "freight")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "price")
