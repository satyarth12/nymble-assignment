from django.shortcuts import get_object_or_404

from .models import *

from drf_yasg import openapi


class TransactionViewsObject:

    def get_item_transaction(self, item_id, user_id):
        # pk = self.kwargs.get(self.lookup)
        pk = item_id
        if pk is not None:

            item = get_object_or_404(Items, pk=pk)
            store = item.store
            # user = get_object_or_404(User, pk=user_id)
            transaction = TransactionBill.objects.filter(
                recipient=user_id, store=store, placed=False)

            return transaction, item


TRANSACTION_REQUEST_BODY = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=['item_id', 'method_type'],
    properties={
        'item_id': openapi.Schema(type=openapi.TYPE_INTEGER),
        'method_type': openapi.Schema(type=openapi.TYPE_STRING)
    },
    description='Item Id to which you want to add in cart'
)
