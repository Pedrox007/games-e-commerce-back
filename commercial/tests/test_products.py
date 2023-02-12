from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from commercial.models import Product


class ProductTestCase(APITestCase):
    url = "/commercial/api/products/"

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
            price=10.50,
            score=500
        )

        self.api_client = APIClient()
        tokens = self._get_tokens()
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens.get("access", None))

    def tearDown(self):
        self.user.delete()
        self.product.delete()

    def test_product_creation(self):
        body = {
            "name": "test product 2",
            "price": 250.50,
            "score": 700
        }

        api_response = self.api_client.post(path=self.url, data=body, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("id" in data.keys(), True)

    def test_product_put(self):
        body = {
            "name": "test product 1",
            "price": 200.00,
            "score": 500
        }
        api_response = self.api_client.put(path="{}{}/".format(self.url, self.product.id), data=body, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(data["price"]), 200.00)

    def test_product_patch(self):
        body = {
            "price": 100.00,
        }
        api_response = self.api_client.patch(path="{}{}/".format(self.url, self.product.id), data=body, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(data["price"]), 100.00)

    def test_product_list(self):
        api_response = self.api_client.get(path=self.url, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data["results"]) > 0, True)

    def test_product_retrieve(self):
        api_response = self.api_client.get(path="{}{}/".format(self.url, self.product.id), json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["id"], self.product.id)

    def test_product_delete(self):
        api_response = self.api_client.delete(path="{}{}/".format(self.url, self.product.id), json=True)

        self.assertEqual(api_response.status_code, status.HTTP_204_NO_CONTENT)
