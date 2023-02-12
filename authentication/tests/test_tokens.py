from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class TokenTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test",
            password="123456",
            email="test@testing.com"
        )

        self.api_client = APIClient()

    def tearDown(self):
        self.user.delete()

    def _get_tokens(self):
        url = "/authentication/api/token/"
        body = {
            "username": "test",
            "password": "123456"
        }
        response = self.api_client.post(path=url, data=body, json=True)

        return response

    def test_token_creation(self):
        api_response = self._get_tokens()
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual("access" in data.keys(), True)
        self.assertEqual("refresh" in data.keys(), True)

    def test_refresh_token(self):
        tokens_data = self._get_tokens().data
        url = "/authentication/api/token/refresh/"
        body = {
            "refresh": tokens_data.get("refresh", None)
        }
        api_response = self.api_client.post(path=url, data=body, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual("access" in data.keys(), True)
