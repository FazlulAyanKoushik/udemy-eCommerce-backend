from django.db import models
from product.models import Product
from account.models import UserProfile
# Create your models here.


class Order(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name="order_by")
    paymentMethod = models.CharField(max_length=100)
    taxPrice = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    shippingPrice = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    totalPrice = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __Str__(self):
        return str(self.user)