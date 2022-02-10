from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token

from rest_framework.test import APITestCase, APIClient
from main_app.models import *
from main_app.serializers import *
from main_app.views import *

from faker import Faker
fake = Faker()
Faker.seed(0)


class AccountTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'satyarth', 'satyarth@dev.com', 'admin@123')
        self.token = Token.objects.create(user=self.user)
        self.auth_header = 'Token ' + self.token.key

        self.header = {'Authorization': self.auth_header}
        self.api_client = APIClient()

        self.store_data = {"owner": self.user.id, "name": "new store",
                           "open_till": fake.future_datetime()}

        self.item_category_data = {"name": "PIZZA"}

        self.item_url = "http://127.0.0.1:8000/app/item/"
        self.store_url = "http://127.0.0.1:8000/app/store/"
        self.item_category_url = "http://127.0.0.1:8000/app/item-category/"

    def test_token_creation(self):
        url = reverse('main_app:api-token-auth')
        data = {
            "username": "satyarth",
            "password": "admin@123"
        }
        self.token_response = self.client.post(url, data=data, format='json')
        self.assertEqual(self.token_response.status_code,
                         status.HTTP_200_OK)

    def test_creating_store(self):
        self.api_client.credentials(HTTP_AUTHORIZATION=self.auth_header)

        self.store_response = self.api_client.post(
            self.store_url, data=self.store_data, format='json')

        self.assertEqual(self.store_response.status_code,
                         status.HTTP_201_CREATED)

    def test_creating_item_category(self):
        self.api_client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        self.item_category_response = self.api_client.post(
            self.item_category_url, data=self.item_category_data, format='json')

        self.assertEqual(self.item_category_response.status_code,
                         status.HTTP_201_CREATED)

    def test_creating_item(self):
        store_data = {"owner": self.user, "name": "new store",
                      "open_till": fake.future_datetime()}
        store = Store.objects.create(**store_data)

        item_cat = ItemCategory.objects.create(**self.item_category_data)

        self.item_data = {"store": store.name, "name": "golden corn pizza",
                          "code": "pizza123", "price": 200.0, "quantity": 20, "type": item_cat.name}

        self.api_client.credentials(HTTP_AUTHORIZATION=self.auth_header)
        self.item_response = self.api_client.post(
            self.item_url, data=self.item_data, format='json')

        self.assertEqual(self.item_response.status_code,
                         status.HTTP_201_CREATED)
