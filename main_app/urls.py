from django.urls import path, include
from rest_framework import routers

from .views import StoreView, ItemView, TransactionBillView, AvgSalesDate, StoreSalesView

router = routers.DefaultRouter()
router.register(r'store', StoreView, basename='store')
router.register(r'item', ItemView, basename='item')
# router.register(r'transaction', TransactionBillView, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),

    path('store-sales-details/',
         StoreSalesView.as_view(), name="store-sales-details"),

    path('my-transactions/',
         TransactionBillView.as_view({'get': 'get_my_transactions'})),
    path('create-update-bill/',
         TransactionBillView.as_view({'post': 'create_update_bill'})),
    path('place-order/<uuid:transaction_id>/',
         TransactionBillView.as_view({'patch': 'place_order'})),

    path('sales-by-date/', AvgSalesDate.as_view())

]
