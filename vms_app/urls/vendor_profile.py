from django.urls import path
from ..views import vpm

urlpatterns = [
    path('', vpm.vendor_list, name='vendor-list'),
    path('<int:pk>/', vpm.vendor_detail, name='vendor-detail'),
]