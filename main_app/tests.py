# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
# from .models import Store, User, Items, ItemCategory, TransactionBill
# from .serializers import SalesSerializer


# class StoreSalesViewTest(APITestCase):

#     def setUpTestData(self):
#         user = User.objects.filter().first()

#         self.store = Store.objects.create(
#             owner=user, name="Branded Store",
#         )
#         self.item_category = ItemCategory.objects.get_or_create(
#             name="PIZZA"
#         )
#         self.item = Items.objects.create(
#             store=self.store,
#             name="chicken pizza",
#             price=200.0,
#             code="chicken_123"
#             quantity=20,
#             type=self.item_category,
#             sale=True
#         )
#         cost = self.item.price*2
#         cart = {
#             self.item: [2, cost, cost]
#         }
#         self.bill = TransactionBill.objects.create(
#             recipient=user,
#             store=self.store,
#             total=self.item.price,
#             cart=cart
#         )
#         self.bill.add(self.item)
#         Items.reduce_quantity(self.item)

#     def test_get_store_sales_details(self):
#         response = client.get(
#             reverse('get_delete_update_puppy', kwargs={'pk': self.rambo.pk}))
#         sales_data = SalesSerializer(User.objects.filter().first())
#         self.assertEqual(response.data, sales_data.data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
