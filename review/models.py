from django.db import models
from product.models import Product
from account.models import UserProfile

# Create your models here.
class Review(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.comment)[0:40]