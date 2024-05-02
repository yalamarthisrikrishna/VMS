import datetime
import uuid

from django.db import models
from django.contrib.postgres.fields import JSONField


class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=100, unique=True, default=uuid.uuid1)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateField()
    delivery_date = models.DateField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50, default='pending')
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(default=datetime.datetime.now)
    acknowledgment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.po_number
