from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from rest_framework.decorators import action


from .filters import SalesFilter
from .serializers import *
from .models import *

from .views_service import TransferBillService
from .util import TransactionViewsObject


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self, request):
        return self.serializer_class(User.objects.get(id=request.user.id)).data


class StoreSalesView(generics.GenericAPIView):
    serializer_class = SalesSerializer
    # filter_class = SalesFilter

    def get(self, request, pk):
        """
        pk -> user_id
        """
        # queries
        from_date = request.GET.get("from_date", None)
        to_date = request.GET.get("to_date", None)
        context = {}
        if from_date and to_date:
            context = {
                "from_date": from_date,
                "to_date": to_date
            }

        return Response(self.serializer_class(User.objects.get(id=pk), context=context).data)


class StoreView(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    filter_class = SalesFilter


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemsSerializer
    queryset = Items.objects.all()


class TransactionBillView(TransactionViewsObject, viewsets.ViewSet):
    serializer_class = TransactionBillSerializer
    queryset = TransactionBill.objects.all()

    def create_update_bill(self, request, operation, *args, **kwargs):
        """POST REQUEST
        """
        data = request.data
        item_id = data.get("item_id")
        user_id = data.get("user_id")

        transaction, item, user = self.get_item_transaction(
            item_id=item_id, user_id=user_id)

        if operation == "create":
            if not transaction:
                result = TransferBillService(
                    item=item, curr_user=user).create_transaction()
                if type(result).__name__ == "TransactionBill":
                    return Response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
                return Response("Item Unavailable", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            func = TransferBillService(
                transaction=transaction, item=item, curr_user=user).update_transaction()
            return Response("UPDATED")

        elif operation == "update":
            if transaction:
                func = TransferBillService(
                    transaction=transaction, item=item, curr_user=user).update_transaction()
                # thread = ThreadPoolExecutor().submit(func.create_update_transaction)
                # result = thread.result()
                return Response("UPDATED")

            result = TransferBillService(
                item=item, curr_user=user).create_transaction()
            if type(result).__name__ == "TransactionBill":
                return Response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
            return Response("Item Unavailable", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
