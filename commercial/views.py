from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, mixins, serializers, filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commercial.models import Cart, Product, Order
from commercial.serializers import CartSerializer, ProductSerializer, OrderSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ["name", "price", "score"]
    filterset_fields = ["name", "price", "score"]


class CartViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Cart.objects.all().prefetch_related("cartitem_set", "cartitem_set__product")
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"], url_path="get-cart")
    def get_cart(self, request):
        queryset = self.get_queryset().filter(user=request.user).order_by("-created_at").first()

        if not queryset:
            return Response({"error": "There isn't cart data for this user."}, status=status.HTTP_404_NOT_FOUND)

        return Response(self.get_serializer(queryset).data)

    @action(detail=False, methods=["delete"], url_path="delete-cart")
    def delete_cart(self, request):
        queryset = self.get_queryset().filter(user=request.user)

        if not queryset:
            return Response({"error": "There isn't cart data for this user."}, status=status.HTTP_404_NOT_FOUND)

        queryset.delete()

        return Response({"message": "Cart deleted."}, status=status.HTTP_202_ACCEPTED)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related("orderitem_set", "orderitem_set__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ["user", "created_at"]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    @extend_schema(request=None)
    @action(detail=False, methods=["post"], url_path="create-order-through-cart")
    def create_order_through_cart(self, request):
        cart_queryset = Cart.objects.filter(user=request.user).order_by("-created_at").first()

        if not cart_queryset:
            return Response({"error": "There isn't cart data for this user."}, status=status.HTTP_404_NOT_FOUND)

        data = {
            "user": self.request.user.id,
            "items": list(cart_queryset.cartitem_set.all().values("product_id", "price")),
            "freight": cart_queryset.total_freight
        }

        order_serializer = self.get_serializer(data=data)
        try:
            order_serializer.is_valid(raise_exception=True)
            order_serializer.save()
        except serializers.ValidationError as errors:
            raise serializers.ValidationError({"order": errors.detail})

        return Response(order_serializer.data)
