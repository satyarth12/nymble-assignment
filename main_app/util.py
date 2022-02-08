import json

from django.contrib.auth import get_user_model
from .serializers import TransactionBillSerializer
from .models import TransactionBill


class PlaceOrders:
    def __init__(self, transaction, item, item_id, curr_user):
        self.transaction = transaction
        self.item = item
        self.item_id = item_id
        self.curr_user = curr_user

    def add(self):
        if self.transaction.exists():
            return

        # new_item = []
        # self.item_count = 1
        # new_item.append(self.item.name)
        # new_item.append(self.item_count)
        # new_item.append(self.item.cost)

        # new_list = {self.item.id: new_item}

        print(self.item)

        instance = TransactionBill.objects.create(
            recipient=self.curr_user, store=self.item.store, total=self.item.price)
        instance.items.add(self.item)
        return instance
