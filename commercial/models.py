from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField("Name", max_length=100, db_index=True)
    price = models.DecimalField("Price", max_digits=20, decimal_places=2)
    score = models.PositiveIntegerField("Score")
    image = models.ImageField("Image", upload_to="images")

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(BaseModel):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Cart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantity")

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"


class Order(BaseModel):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Cart", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantity")
    freight = models.DecimalField("Freight", max_digits=20, decimal_places=2)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"
