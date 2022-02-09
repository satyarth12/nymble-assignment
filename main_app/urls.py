from django.urls import path, include
from rest_framework import routers

from .views import StoreView, ItemView, TransactionBillView, UserView, StoreSalesView

router = routers.DefaultRouter()
router.register(r'store', StoreView, basename='store')
router.register(r'item', ItemView, basename='item')
# router.register(r'transaction', TransactionBillView, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),

    path('store-sales-details/<int:pk>/',
         StoreSalesView.as_view()),

    path('create-update-bill/',
         TransactionBillView.as_view({'post': 'create_update_bill'})),

]
