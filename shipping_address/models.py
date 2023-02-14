from django.db import models
from order.models import Order

# Create your models here.
class ShippingAddress(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, blank=True, null=True, related_name='shipping_address')
    address = models.CharField(max_length=255,blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    postalCode = models.CharField(max_length=255,blank=True, null=True)
    country = models.CharField(max_length=255,blank=True, null=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=1, blank=True, null=True)

    def __Str__(self):
        return str(self.address)[0:40]