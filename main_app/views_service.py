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
    def decrease_delete_item(tb_instance, item_instance):
        with transaction.atomic():
            key_ = str(item_instance)

            count = tb_instance.cart[key_][0] - 1

            # if item's count is 0
            if count == 0:
                tb_instance.cart.pop(key_)
                tb_instance.items.remove(item_instance)
                new_cart = tb_instance.cart
                ini_total = tb_instance.total
                item_cost = item_instance.price

                # if cart is empty then delete the transaction
                if bool(new_cart) == False:
                    # increasing item's quantity availability
                    Items.increase_quantity(instance=item_instance)
                    tb_instance.delete()
                    return 'Transaction Deleted'

                tb_instance.cart = new_cart
                tb_instance.total = ini_total - item_cost
                tb_instance.save()

                # increasing item's quantity availability
                Items.increase_quantity(instance=item_instance)

                return 'Item Removed'

            # update the cart
            ini_total = tb_instance.total
            item_cost = item_instance.price
            tb_instance.total = ini_total - item_cost
            tb_instance.cart[key_][0] = count
            tb_instance.cart[key_][2] = count*item_cost
            tb_instance.save()

            # increasing item's quantity availability
            Items.increase_quantity(instance=item_instance)

            return "Decreased"

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

            # updating an item already present in existing cart
            if operation == "increase_item":
                count = tb_instance.cart[key_][0] + 1
                total_item_cost_ = tb_instance.cart[key_][1] + \
                    tb_instance.cart[key_][2]

                tb_instance.cart[key_][0] = count  # update item_count + 1

                # update item's total cost in cart
                tb_instance.cart[key_][2] = total_item_cost_
                total_cart_cost = tb_instance.total + item_instance.price

            # adding an item in the existing cart
            elif operation == "add_item":
                count = 1
                tb_instance.cart[key_] = [
                    count, item_instance.price, item_instance.price]
                tb_instance.items.add(item_instance)

                total_cart_cost = tb_instance.total + item_instance.price

            # updating transaction's total cost
            tb_instance.total = total_cart_cost
            tb_instance.save()

            # updating Item instance's availability
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
                instance.items.add(self.item)
                Items.reduce_quantity(instance=self.item)
                return instance
        except Exception as e:
            return e

    def add_increase_transaction(self):
        """Increase the item's quantity in the cart if already there
        else adds item in the cart
        """
        transaction_instance = self.transaction

        # increase item quantity in the json cart if already present in the unplaced transaction
        if str(self.item) not in transaction_instance.cart.keys():
            result = self.increase_add_item(
                operation="add_item", tb_instance=transaction_instance, item_instance=self.item)
            return result
        else:
            result = self.increase_add_item("increase_item", transaction_instance,
                                            self.item)
            return result

    def decrease_delete_transaction(self):
        """Decrease/Deletes the item from the cart.
        If cart is empty the deletes the transaction.
        """
        transaction_instance = self.transaction

        if str(self.item) in transaction_instance.cart.keys():
            result = self.decrease_delete_item(
                tb_instance=transaction_instance, item_instance=self.item)
            return result
        return False
