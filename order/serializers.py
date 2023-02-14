from rest_framework import serializers
from .models import Order
from shipping_address.models import ShippingAddress
from order_item.models import OrderItem
from account.models import UserProfile
from account.serializers import UserSerializer
from product.models import Product

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'email', 'first_name']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['_id', 'name', 'brand', 'category','price']

class OrderItemSerializer(serializers.ModelSerializer):
    """
        If you want product object instead of product id, then uncomment it
    """
    # product = ProductSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = '__all__'
        # fields = ['_id', 'product', 'order', 'name', 'quantity', 'price', 'image']

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    shipping_address = ShippingAddressSerializer(many=False, read_only=True)
    user=UserSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
