from django.urls import path, include
from rest_framework import routers

from .views import StoreView, ItemView, TransactionBillView

router = routers.DefaultRouter()
router.register(r'store', StoreView, basename='store')
router.register(r'item', ItemView, basename='item')
# router.register(r'transaction', TransactionBillView, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
    path('add_item/', TransactionBillView.as_view({'post': 'add_item'}))
]
