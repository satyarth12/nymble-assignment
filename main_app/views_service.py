import json

from django.contrib.auth.models import User
from .models import TransactionBill, Items
from concurrent.futures import ThreadPoolExecutor
from django.db import transaction


class TransferBillService:
    def __init__(self, transaction=None, item=None, curr_user=None):
        self.transaction = transaction  # queryset of available TransactionBills
        self.item = item  # single item instance
        self.item_id = self.item.id  # item instance id
        self.curr_user = curr_user  # current logged in user

    @staticmethod
    def increase_add_item(operation: str, tb_instance, item_instance):
        """Increase Item Quantity Or Add new item in the json cart
        # {"item_instance": [item_count->int,
        # item_cost->int,
        # total_cost->float]}
        """
        with transaction.atomic():

            total_cart_cost = 0
            key_ = str(item_instance)

            # updating an item already in cart
            if operation == "increase_item":

                print("INCREASE")
                cart_obj = tb_instance.cart[key_]
                count = tb_instance.cart[key_][0] + 1
                item_cost_ = tb_instance.cart[key_][1] + \
                    tb_instance.cart[key_][2]

                tb_instance.cart[key_][0] = count  # update item_count + 1

                # update item's total cost in cart

                tb_instance.cart[key_][2] = item_cost_
                print(tb_instance.cart[key_][2])
                for key, value in tb_instance.cart.items():
                    total_cart_cost += tb_instance.cart[key][2]

            # adding an item in the cart
            elif operation == "add_item":
                print("ADD")
                count = 1
                tb_instance.cart[key_] = [
                    count, item_instance.price, item_instance.price]

                for key, value in tb_instance.cart.items():
                    print(value)
                    total_cart_cost += tb_instance.cart[key][2]

            print(total_cart_cost)
            tb_instance.total = total_cart_cost
            tb_instance.save()

            # updating Item instance
            Items.reduce_quantity(instance=item_instance)

        return tb_instance

    def create_transaction(self):
        """Create TransactionBill
        """
        value_list = []
        key_ = str(self.item)
        item_count = 0
        value_list.extend([item_count+1, self.item.price, self.item.price])
        cart_ = {key_: value_list}
        total_ = cart_[key_][2]

        try:
            with transaction.atomic():
                instance = TransactionBill.objects.create(
                    recipient=self.curr_user,
                    store=self.item.store,
                    cart=cart_,
                    total=total_)
                Items.reduce_quantity(instance=self.item)
                return instance
        except Exception as e:
            return e

    def update_transaction(self):
        transaction_instance = self.transaction.first()

        # increase item quantity in the json cart if already present in the unplaced transaction
        if str(self.item) not in transaction_instance.cart.keys():
            print("sdhbfhdbfk")
            result = self.increase_add_item(
                operation="add_item", tb_instance=transaction_instance, item_instance=self.item)
            return result
        else:
            print("jkdbfkhj")
            result = self.increase_add_item("increase_item", transaction_instance,
                                            self.item)
            return result