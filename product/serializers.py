from product.models import Product
from rest_framework.serializers import ModelSerializer
from account.models import UserProfile
from review.models import Review
from review.serializers import ReviewSerializer



class  ProductSerializer(ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True, source='review_set')
    class Meta:
        model = Product
        fields = '__all__'




class  ProductUpdateSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price', 'brand', 'countInStock', 'category', 'description']




