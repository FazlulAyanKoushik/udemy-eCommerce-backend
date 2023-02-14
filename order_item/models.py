from django.db import models
from product.models import Product
from order.models import Order
# Create your models here.
class OrderItem(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, related_name='order_items')
    name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    image = models.CharField(max_length=255, blank=True, null=True)

    def __Str__(self):
        return str(self.name)