
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema


from .permission import IsItemOwnerOrReadOnly, IsStoreOwner
from .serializers import *
from .models import *

from .views_service import TransferBillService
from .util import TransactionViewsObject, TRANSACTION_REQUEST_BODY


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self, request):
        return self.serializer_class(User.objects.get(id=request.user.id)).data


class StoreSalesView(generics.GenericAPIView):
    serializer_class = SalesSerializer

    def get(self, request):
        """fetch the store-meta-details of the current user's store
        """
        try:
            return Response(self.serializer_class(User.objects.get(id=request.user.id)).data)
        except Exception as e:
            return Response(e)


class StoreView(viewsets.ModelViewSet):
    serializer_class = StoreSerializer
    permission_classes = [IsStoreOwner]
    queryset = Store.objects.all()


class ItemView(viewsets.ModelViewSet):
    serializer_class = ItemsSerializer
    permission_classes = [IsItemOwnerOrReadOnly]
    queryset = Items.objects.all()


class TransactionBillView(TransactionViewsObject, viewsets.ViewSet):
    serializer_class = TransactionBillSerializer
    queryset = TransactionBill.objects.all()

    @swagger_auto_schema(request_body=TRANSACTION_REQUEST_BODY)
    def create_update_bill(self, request, *args, **kwargs):
        """POST REQUEST
        """
        data = request.data
        item_id = data.get("item_id")
        method_type = data.get("method_type", None)
        user = self.request.user

        transaction, item = self.get_item_transaction(
            item_id=item_id, user_id=user.id)

        if not transaction and method_type == "create":
            """creates a new transaction instance if create=True
            """
            result = TransferBillService(
                item=item, curr_user=user).create_transaction()
            if type(result).__name__ == "TransactionBill":
                return Response(self.serializer_class(result).data, status=status.HTTP_201_CREATED)
            return Response("Item Unavailable", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        elif transaction and method_type == "update_increase":
            """Increases item's quantity / add an item in the pre existing transaction
            """
            if transaction.recipient == request.user:
                result = TransferBillService(
                    transaction=transaction, item=item, curr_user=user).add_increase_transaction()
                return Response(self.serializer_class(result).data)
            return Response("Not Authorized to edit", status=status.HTTP_403_FORBIDDEN)

        elif transaction and method_type == "update_decrease":
            """Decreases item's quantity / remoces an item from the pre existing transaction
            """
            if transaction.recipient == request.user:
                result = TransferBillService(
                    transaction=transaction, item=item, curr_user=user).decrease_delete_transaction()
                if result:
                    return Response(result)
                return Response("Item not in cart", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            return Response("Not Authorized to edit", status=status.HTTP_403_FORBIDDEN)
