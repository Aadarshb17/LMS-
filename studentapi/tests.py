from django.test import TestCase
import factory
from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.urls import reverse
from lmsapp.models import *
from rest_framework import status
from faker import Faker
from django.contrib.auth.hashers import make_password
import json

# pwd = factory.Faker('password')
passw = Faker().password()
# Create your tests here.
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        # django_get_or_create = ('username', 'password', 'email')

    username = factory.Faker("user_name")
    # pwd= factory.Faker('password')
    email = factory.Faker("email")
    password = factory.LazyFunction(lambda: make_password(passw))

    # @classmethod
    # def create(cls, *args, **kwargs):
    #     user = User.objects.create_user(username='abd', password='2343', email='ab@gmail.com')
    #     return user


class TokenTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()

    def test_token_jwt(self):
        data = {"username": self.user.username, "password": passw}

        response = self.client.post(reverse("token_obtain_pair"), data, format="json")
        self.token = response.content
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.token)
        return self.token


class RefreshTokenTest(TokenTest):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        # breakpoint()
        self.data = self.test_token_jwt()

    def test_refreshtoken_jwt(self):
        # breakpoint()
        refresh_token = {"refresh": json.loads(self.data)["refresh"]}
        response = self.client.post(
            reverse("token_refresh"), refresh_token, format="json"
        )
        # breakpoint()
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LogoutTokenTest(TokenTest):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.data = self.test_token_jwt()

    def test_logtouttoken_jwt(self):
        refresh_token = {"refresh": json.loads(self.data)["refresh"]}
        response = self.client.post(
            reverse("token_blacklist"), refresh_token, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
