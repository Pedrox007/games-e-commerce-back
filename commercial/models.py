from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, DecimalField, Value
from django.db.models.functions import Coalesce


class BaseModel(models.Model):
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    name = models.CharField("Name", max_length=100, db_index=True)
    price = models.DecimalField("Price", max_digits=20, decimal_places=2)
    score = models.PositiveIntegerField("Score", blank=True, null=True)
    image = models.ImageField("Image", upload_to="images", blank=True, null=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Cart(BaseModel):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    @property
    def subtotal_price(self):
        subtotal_price = self.cartitem_set.aggregate(
            subtotal_price=Coalesce(
                Sum("price"),
                Value(0),
                output_field=DecimalField(max_digits=14, decimal_places=2)
            )
        )["subtotal_price"]

        return float(subtotal_price)

    @property
    def total_freight(self):
        total_freight = self.cartitem_set.count() * float(settings.FREIGHT_PRICE) if self.subtotal_price < 250 else 0

        return total_freight

    @property
    def total_price(self):
        total_price = self.subtotal_price + self.total_freight

        return total_price


class CartItem(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    price = models.DecimalField("Price", max_digits=20, decimal_places=2, default=0)
    cart = models.ForeignKey(Cart, verbose_name="Cart", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.price:
            self.price = self.product.price

        return super(CartItem, self).save(force_insert, force_update, using, update_fields)


class Order(BaseModel):
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)
    freight = models.DecimalField("Freight", max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    @property
    def subtotal_price(self):
        subtotal_price = self.orderitem_set.aggregate(
            subtotal_price=Coalesce(
                Sum("price"),
                Value(0),
                output_field=DecimalField(max_digits=14, decimal_places=2)
            )
        )["subtotal_price"]

        return subtotal_price

    @property
    def total_price(self):
        total_price = self.subtotal_price + self.freight

        return total_price


class OrderItem(BaseModel):
    product = models.ForeignKey(Product, verbose_name="Product", on_delete=models.CASCADE)
    order = models.ForeignKey(Order, verbose_name="Order", on_delete=models.CASCADE)
    price = models.DecimalField("Price", max_digits=20, decimal_places=2, default=0)

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.price:
            self.price = self.product.price

        return super(OrderItem, self).save(force_insert, force_update, using, update_fields)
