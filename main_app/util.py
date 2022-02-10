from django.shortcuts import get_object_or_404

from .models import *

from drf_yasg import openapi


class TransactionViewsObject:

    def get_item_transaction(self, item_id, user_id):
        if item_id is not None:

            item = get_object_or_404(Items, pk=item_id)
            store = item.store
            transaction = TransactionBill.objects.filter(
                recipient=user_id, store=store, placed=False).first()

            return transaction, item


PLACED_QUERY_PARAM = openapi.Parameter(
    'placed', openapi.IN_QUERY, description="Placed boolean parameter", type=openapi.TYPE_BOOLEAN)


TRANSACTION_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['item_id', 'method_type'],
    properties={
        'item_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Item Id to which you want to add in cart'),
        'method_type': openapi.Schema(type=openapi.TYPE_STRING, description='''method_type: create, to create a transaction instance
                                                                method_type: update_increase, to increase item's quantity / add an item in an existing transaction
                                                                method_type: update_decrease, to decrease item's quantity / removes an item from an existing transaction''')
    },
)
