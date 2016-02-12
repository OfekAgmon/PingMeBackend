from django.db import models
from decimal import Decimal



class Device(models.Model):
    device_id = models.CharField(unique = True, max_length = 1024, default='')
    user = models.ForeignKey('auth.User', null=True)

class Location(models.Model):
    user = models.ForeignKey('auth.User', null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, default=Decimal('0.00'))
    longitude = models.DecimalField(max_digits=10, decimal_places=7, default=Decimal('0.00'))