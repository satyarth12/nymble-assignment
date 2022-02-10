
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from django.utils import timezone

from .permission import IsItemOwnerOrReadOnly, IsStoreOwner
from .serializers import *
from .models import *

from .views_service import TransferBillService
from .util import TransactionViewsObject, TRANSACTION_REQUEST_BODY, PLACED_QUERY_PARAM


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self, request):
        return self.serializer_class(User.objects.get(id=request.user.id)).data


class StoreSalesView(generics.GenericAPIView):
    serializer_class = SalesSerializer

    def get(self, request):
        """fetch the store-meta-details of the current user's store
        """
        user = request.user
        if Store.objects.filter(owner=user).exists():
            return Response(self.serializer_class(User.objects.get(id=user.id)).data)
        return Response("You have no store registered with you. Create one please", status=status.HTTP_404_NOT_FOUND)


# TODO:
# class AvgSalesDate(generics.GenericAPIView):
#     serializer_class = SalesSerializer

#     def get(self, request):
#         store = request.user.store_owner
#         print(store)
#         from_date = request.data.get("from_date", None)
#         to_date = request.data.get("to_date", None)

#         store_transactions = TransactionBill.objects.select_related(
#             "store").filter(store=store, placed_timestamp__date__range=[from_date, to_date])

#         print(store_transactions)
#         return Response(self.serializer_class(store_transactions.user, many=True).data)


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

    @swagger_auto_schema(manual_parameters=[PLACED_QUERY_PARAM])
    def get_my_transactions(self, request):
        """Gives the Transactions list made by current logged in user
        """
        user = self.request.user
        # without capitalize(), django.core.exceptions.ValidationError: ['“false” value must be either True or False.']
        placed_ = request.GET.get('placed').capitalize()

        transactions = TransactionBill.objects.select_related(
            "recipient").filter(recipient=user, placed=placed_)
        return Response(self.serializer_class(transactions, many=True).data)

    @swagger_auto_schema(request_body=TRANSACTION_REQUEST_BODY)
    def create_update_bill(self, request, *args, **kwargs):
        """POST REQUEST
        """
        data = request.data
        item_id = data.get("item_id")
        method_type = data.get("method_type", None)
        user = self.request.user

        # getting valid transaction and item instances, if present, for further validation.
        transaction, item = self.get_item_transaction(
            item_id=item_id, user_id=user.id)

        if timezone.now() < item.store.open_till:  # if store closing time hasn't exceeded

            if not transaction and method_type == "create":
                """creates a new transaction instance
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
                    if not transaction.placed:  # placed transactions are not allowed to be edited
                        result = TransferBillService(
                            transaction=transaction, item=item, curr_user=user).add_increase_transaction()
                        return Response(self.serializer_class(result).data)
                    return Response("Items are already placed", status=status.HTTP_208_ALREADY_REPORTED)
                return Response("Not Authorized to edit", status=status.HTTP_403_FORBIDDEN)

            elif transaction and method_type == "update_decrease":
                """Decreases item's quantity / remoces an item from the pre existing transaction
                """
                if transaction.recipient == request.user:
                    if not transaction.placed:  # placed transactions are not allowed to be edited
                        result = TransferBillService(
                            transaction=transaction, item=item, curr_user=user).decrease_delete_transaction()
                        if result:
                            return Response(result)
                        return Response("Item not in cart", status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                    return Response("Items are already placed", status=status.HTTP_208_ALREADY_REPORTED)
                return Response("Not Authorized to edit", status=status.HTTP_403_FORBIDDEN)

            return Response("Error with form data", status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response("Store's closed", status=status.HTTP_423_LOCKED)

    def place_order(self, request, transaction_id):
        instance = get_object_or_404(TransactionBill, id=transaction_id)

        if instance.recipient == request.user:
            if not instance.placed:
                instance.placed = True
                instance.save()
            return Response("Items placed successfully", status=status.HTTP_200_OK)
        return Response("Not Authorized", status=status.HTTP_403_FORBIDDEN)
