import imp
from random import random
from django.core.management.base import BaseCommand
from faker import Faker
import faker.providers

from main_app.models import *
from django.contrib.auth.models import User
from django.db import transaction

from main_app.management.helpers import store_data, user_data, item_data

USER = User.objects.all()


class Provider(faker.providers.BaseProvider):
    def user_(self):
        return self.random_element(list(USER))


class Command(BaseCommand):
    help = "Command To create main_app's model data"

    def handle(self, *args, **kwargs):
        """
        Module to run the Command
        """
        fake = Faker()
        fake.add_provider(Provider)

        store_list = []
        with transaction.atomic():

            item_category = [ItemCategory(
                name="PIZZA"), ItemCategory(name="BURGER")]
            ItemCategory.objects.bulk_create(item_category)

            super_user = User.objects.create_superuser(
                username="admin", password="admin@123", email="admin@dev.com")

            for i in range(5):
                user = user_data(fake_=fake)
                store = store_data(owner_=user, i=i, fake_=fake)

                store_list.append(store)

            item = item_data(stores=store_list,
                             item_category=item_category, fake_=fake)
