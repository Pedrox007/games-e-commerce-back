import json

from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from commercial.models import Product, Cart, CartItem


class CartTestCase(APITestCase):
    url = "/commercial/api/carts/"

    def _get_tokens(self):
        url = "/authentication/api/token/"
        body = {
            "username": "test",
            "password": "123456"
        }
        response_data = self.api_client.post(path=url, data=body, json=True).data

        return response_data

    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="123456",
            email="test@testing.com"
        )

        self.product = Product.objects.create(
            name="test product",
            price=200.00,
            score=500
        )

        self.cart = Cart.objects.create(user=self.user)

        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product)

        self.api_client = APIClient()
        tokens = self._get_tokens()
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens.get("access", None))

    def tearDown(self):
        self.user.delete()
        self.product.delete()
        self.cart.delete()
        self.cart_item.delete()

    def test_cart_creation_with_freight(self):
        body = {
            "user": self.user.id,
            "items": [
                {"product_id": self.product.id}
            ]
        }

        api_response = self.api_client.post(
            path=self.url,
            data=json.dumps(body),
            json=True,
            content_type="application/json"
        )
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("id" in data.keys(), True)
        self.assertEqual(data["total_freight"], float(settings.FREIGHT_PRICE))

    def test_cart_creation_without_freight(self):
        body = {
            "user": self.user.id,
            "items": [
                {"product_id": self.product.id},
                {"product_id": self.product.id}
            ]
        }

        api_response = self.api_client.post(
            path=self.url,
            data=json.dumps(body),
            json=True,
            content_type="application/json"
        )
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("id" in data.keys(), True)
        self.assertEqual(data["total_freight"], 0)

    def test_cart_put(self):
        body = {
            "user": self.user.id,
            "items": [
                {"product_id": self.product.id},
                {"product_id": self.product.id}
            ]
        }
        api_response = self.api_client.put(
            path="{}{}/".format(self.url, self.cart.id),
            data=json.dumps(body),
            json=True,
            content_type="application/json"
        )
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["items"]), 2)

    def test_cart_patch(self):
        body = {
            "items": [
                {"product_id": self.product.id},
                {"product_id": self.product.id}
            ]
        }
        api_response = self.api_client.patch(
            path="{}{}/".format(self.url, self.cart.id),
            data=json.dumps(body),
            json=True,
            content_type="application/json"
        )
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["items"]), 2)

    def test_cart_retrieve(self):
        api_response = self.api_client.get(path="{}get-cart/".format(self.url), json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], self.cart.id)

    def test_cart_delete(self):
        api_response = self.api_client.delete(path="{}delete-cart/".format(self.url), json=True)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
