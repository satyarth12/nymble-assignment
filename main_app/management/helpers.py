import json
import random
from faker import Faker
import itertools

from main_app.models import *


def zip_multiple_element(l: list, o):
    """Zip list with a single element
    """
    return zip(l, itertools.repeat(o))


item_list = ['pepproni pizza', 'golden ccorn pizza',
             'kfc burger', 'veg burgger',  'maharaja mac burger']


store_names = ['KFC', 'Brewri Cafe', 'McDonalds',
               'Park Street Cafe', '24*7 Dhabha']


def user_data(fake_):
    username = fake_.first_name()
    email = fake_.email()
    password = "User@123"

    user = User.objects.create_user(
        username=username, email=email, password=password)

    file = open("config/usernames.txt", "a")
    file.write(username+"\n")
    file.close()
    return user


def store_data(owner_, i, fake_):
    """Creates Store Data
    """
    owner = owner_
    name = store_names[i]
    store_time = fake_.future_datetime()

    return Store.objects.create(owner=owner, name=name, open_till=store_time)


def item_data(stores: list, item_category: list, fake_):
    """Creates item instances using stores and item_category in relation
    """
    for index, store in enumerate(stores):
        Items.objects.create(store=store, name=item_list[index],
                             code=fake_.random_number(digits=8),
                             price=fake_.random_number(digits=3),
                             quantity=fake_.random_number(digits=2),
                             type=random.choice(item_category))
