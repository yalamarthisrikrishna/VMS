from django.contrib import admin
from .models.vendor import Vendor
from .models.purchase_order import PurchaseOrder
from .models.historical_performance import HistoricalPerformance

# Register your models here.

admin.site.register(Vendor)
admin.site.register(PurchaseOrder)
admin.site.register(HistoricalPerformance)
