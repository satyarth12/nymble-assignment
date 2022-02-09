from django.shortcuts import get_object_or_404

from .models import *


class TransactionViewsObject:

    def get_item_transaction(self, item_id, user_id):
        # pk = self.kwargs.get(self.lookup)
        pk = item_id
        if pk is not None:

            item = get_object_or_404(Items, pk=pk)
            store = item.store
            user = get_object_or_404(User, pk=user_id)
            transaction = TransactionBill.objects.filter(
                recipient=user_id, store=store, placed=False)

            return transaction, item, user
