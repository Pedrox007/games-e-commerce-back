from django.urls import path, include
from rest_framework.routers import DefaultRouter

from commercial.views import ProductViewSet, CartViewSet, OrderViewSet

router = DefaultRouter()

router.register("api/products", ProductViewSet)
router.register("api/carts", CartViewSet)
router.register("api/orders", OrderViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
