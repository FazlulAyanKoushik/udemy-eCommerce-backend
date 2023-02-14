from django.conf import settings
from django.db import models
from account.models import UserProfile
# Create your models here.


def upload_image(instance, filename):
    return "uploads/{user}/{filename}".format(user=instance.seller, filename=filename)


class Product(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    seller = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True, default='images/placeholder.jpg')
    brand = models.CharField(max_length=255, blank=True, null=True)
    category = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    numReview = models.IntegerField(blank=True, null=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    countInStock = models.IntegerField(blank=True, null=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return str(self.name)[0:30]