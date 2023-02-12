import decimal

from django.db import transaction
from rest_framework import serializers

from commercial.models import Product, CartItem, Cart, OrderItem, Order


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    cart_id = serializers.PrimaryKeyRelatedField(queryset=Cart.objects.all(), source="cart", write_only=True)

    class Meta:
        model = CartItem
        exclude = ["cart"]


class NestedCartItemSerializer(CartItemSerializer):
    id = serializers.IntegerField(required=False)
    cart_id = serializers.PrimaryKeyRelatedField(source="cart", read_only=True)

    class Meta:
        model = CartItem
        exclude = ["cart"]


class CartSerializer(serializers.ModelSerializer):
    items = NestedCartItemSerializer(source="cartitem_set", required=False, many=True)
    subtotal_price = serializers.SerializerMethodField()
    total_freight = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = "__all__"

    def get_subtotal_price(self, obj) -> float:
        return obj.subtotal_price

    def get_total_freight(self, obj) -> float:
        return obj.total_freight

    def get_total_price(self, obj) -> float:
        return obj.total_price

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("cartitem_set", None)
        instance = super().create(validated_data)

        if not items_data:
            return instance

        if items_data:
            serializer = CartItemSerializer(
                data=[
                    {**data, "cart_id": instance.id, "product_id": data.get("product").id}
                    for data in items_data
                ],
                many=True,
                context=self.context,
            )
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except serializers.ValidationError as errors:
                raise serializers.ValidationError({"items": errors.detail})

        return instance

    @transaction.atomic
    def update(self, instance: Cart, validated_data):
        items_data = validated_data.pop("cartitem_set", None)
        instance = super().update(instance, validated_data)

        if items_data is None:
            return instance

        items_ids = [data["id"] for data in items_data if "id" in data]
        instance.cartitem_set.exclude(id__in=items_ids).delete()

        errors = []
        for i, data in enumerate(items_data):
            item_id = data.pop("id", None)
            try:
                cart_item = CartItem.objects.get(id=item_id)
                serializer = CartItemSerializer(
                    instance=cart_item,
                    data={**data, "cart_id": instance.id, "product_id": data.get("product").id},
                    context=self.context,
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except CartItem.DoesNotExist:
                if item_id is None:
                    try:
                        serializer = CartItemSerializer(
                            data={
                                **data,
                                "cart_id": instance.id,
                                "product_id": data.get("product").id
                            },
                            context=self.context,
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    except serializers.ValidationError as err:
                        errors.append(err.detail)
                else:
                    errors.append({"id": "Item does not exist."})
            except serializers.ValidationError as err:
                errors.append(err.detail)

        if len(errors):
            raise serializers.ValidationError({"items": errors})

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source="product", write_only=True)
    order_id = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), source="order", write_only=True)

    class Meta:
        model = OrderItem
        exclude = ["order"]


class NestedOrderItemSerializer(OrderItemSerializer):
    id = serializers.IntegerField(required=False)
    order_id = serializers.PrimaryKeyRelatedField(source="order", read_only=True)

    class Meta:
        model = OrderItem
        exclude = ["order"]


class OrderSerializer(serializers.ModelSerializer):
    items = NestedOrderItemSerializer(source="orderitem_set", required=False, many=True)
    subtotal_price = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_subtotal_price(self, obj) -> decimal.Decimal:
        return obj.subtotal_price

    def get_total_price(self, obj) -> decimal.Decimal:
        return obj.total_price

    @transaction.atomic
    def create(self, validated_data):
        items_data = validated_data.pop("orderitem_set", None)
        instance = super().create(validated_data)

        if not items_data:
            return instance

        if items_data:
            serializer = OrderItemSerializer(
                data=[
                    {**data, "order_id": instance.id, "product_id": data.get("product").id}
                    for data in items_data
                ],
                many=True,
                context=self.context,
            )
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except serializers.ValidationError as errors:
                raise serializers.ValidationError({"items": errors.detail})

        Cart.objects.filter(user=instance.user).delete()

        return instance

    @transaction.atomic
    def update(self, instance: Order, validated_data):
        items_data = validated_data.pop("orderitem_set", None)
        instance = super().update(instance, validated_data)

        if items_data is None:
            return instance

        items_ids = [data["id"] for data in items_data if "id" in data]
        instance.orderitem_set.exclude(id__in=items_ids).delete()

        errors = []
        for i, data in enumerate(items_data):
            item_id = data.pop("id", None)
            try:
                cart_item = OrderItem.objects.get(id=item_id)
                serializer = OrderItemSerializer(
                    instance=cart_item,
                    data={**data, "order_id": instance.id, "product_id": data.get("product").id},
                    context=self.context,
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except OrderItem.DoesNotExist:
                if item_id is None:
                    try:
                        serializer = OrderItemSerializer(
                            data={
                                **data,
                                "order_id": instance.id,
                                "product_id": data.get("product").id
                            },
                            context=self.context,
                        )
                        serializer.is_valid(raise_exception=True)
                        serializer.save()
                    except serializers.ValidationError as err:
                        errors.append(err.detail)
                else:
                    errors.append({"id": "Item does not exist."})
            except serializers.ValidationError as err:
                errors.append(err.detail)

        if len(errors):
            raise serializers.ValidationError({"items": errors})

        return instance
