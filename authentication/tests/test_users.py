from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class UserTestCase(APITestCase):
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
        response_data = self.api_client.post(path=url, data=body, json=True).data

        return response_data

    def test_user_creation(self):
        url = "/authentication/api/users/"
        body = {
            "username": "testing",
            "email": "testing@test.com",
            "password": "mnop1234$",
            "password_confirmation": "mnop1234$",
            "first_name": "testing",
            "last_name": "testing",
        }
        api_response = self.api_client.post(path=url, data=body, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual("username" in data.keys(), True)
        self.assertEqual("password" not in data.keys(), True)

    def test_user_retrieve(self):
        url = "/authentication/api/users/{}/".format(self.user.id)
        tokens = self._get_tokens()
        self.api_client.credentials(HTTP_AUTHORIZATION="Bearer " + tokens.get("access", None))
        api_response = self.api_client.get(path=url, json=True)
        data = api_response.data

        self.assertEqual(api_response.status_code, status.HTTP_200_OK)
        self.assertEqual("username" in data.keys(), True)
        self.assertEqual("password" not in data.keys(), True)
