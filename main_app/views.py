from re import I
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializers import *
from .models import *

from concurrent.futures import ThreadPoolExecutor
from .util import PlaceOrders


class StoreView(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemsSerializer
    queryset = Items.objects.all()


class OrderObject(object):
    # lookup = 'pk'

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


class TransactionBillView(OrderObject, viewsets.ViewSet):
    serializer_class = TransactionBillSerializer
    queryset = TransactionBill.objects.all()

    def add_item(self, request, *args, **kwargs):
        data = request.data
        item_id = data.get("item_id")
        user_id = data.get("user_id")

        transaction, item, user = self.get_item_transaction(
            item_id=item_id, user_id=user_id)

        func = PlaceOrders(transaction, item, item_id, user)
        thread = ThreadPoolExecutor().submit(func.add)
        result = thread.result()
        return Response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
