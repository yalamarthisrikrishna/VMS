# urls.py
from django.urls import path
from ..views import pom

urlpatterns = [
    path('', pom.purchase_order_list, name='purchase-order-list'),
    path('<int:pk>/', pom.purchase_order_detail, name='purchase-order-detail'),
]
