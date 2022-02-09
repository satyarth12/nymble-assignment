from django.urls import path, include
from rest_framework import routers

from .views import StoreView, ItemView, TransactionBillView, UserView, StoreSalesView

router = routers.DefaultRouter()
router.register(r'store', StoreView, basename='store')
router.register(r'item', ItemView, basename='item')
# router.register(r'transaction', TransactionBillView, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),

    path('store-meta-details/<int:pk>/',
         StoreSalesView.as_view()),

    path('create_update_bill/<str:operation>/',
         TransactionBillView.as_view({'post': 'create_update_bill'})),

    # path('user/store-avg-sales/<int:pk>/',
    #      UserView.as_view({"get": "avg_sales"})),
]
