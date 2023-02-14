import json
from django.http import Http404
from datetime import datetime


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .models import Order
from order_item.models import OrderItem
from shipping_address.models import ShippingAddress
from product.models import Product
from .serializers import OrderSerializer



# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrder(request):
    user = request.user
    data = request.data

    order_items = data['orderItems']
    if order_items and len(order_items) == 0:
        return Response({'detail': 'No Order Items added'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # Create order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # Create Shipping Address
        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )
        # Create orderItems Address
        for item in order_items:
            product = Product.objects.get(_id=item['product'])

            orderItem = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                quantity=item['qty'],
                price=product.price,
                image=product.image

            )

            # update Product Stock
            product.countInStock -= orderItem.quantity
            product.save()

        serializer = OrderSerializer(order, many=False)

        print(json.dumps(serializer.data, indent=4))

        return Response(serializer.data)



'''
    Class based Views
'''
permission_classes([IsAuthenticated])
class OrderList(APIView):

    #  get user orders View
    def get(self, request, format=None):
        user = request.user
        try:
            # get all order from user object by related_name "order_by"
            orders = user.order_by.all()
        except:
            return Response({'detail':'No Order Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
        # return Response([])

    # add user order view
    def post(self, request, format=None):
        user = request.user
        data = request.data

        order_items = data['orderItems']
        if order_items and len(order_items) == 0:
            return Response({'detail': 'No Order Items added'}, status=status.HTTP_400_BAD_REQUEST)
        else:

            # Create order
            order = Order.objects.create(
                user=user,
                paymentMethod=data['paymentMethod'],
                taxPrice=data['taxPrice'],
                shippingPrice=data['shippingPrice'],
                totalPrice=data['totalPrice']
            )

            # Create Shipping Address
            shipping = ShippingAddress.objects.create(
                order=order,
                address=data['shippingAddress']['address'],
                city=data['shippingAddress']['city'],
                postalCode=data['shippingAddress']['postalCode'],
                country=data['shippingAddress']['country'],
            )
            # Create orderItems Address
            for item in order_items:
                product = Product.objects.get(_id=item['product'])

                orderItem = OrderItem.objects.create(
                    product=product,
                    order=order,
                    name=product.name,
                    quantity=item['qty'],
                    price=product.price,
                    image=item['image']

                )

                # update Product Stock
                product.countInStock -= orderItem.quantity
                product.save()

            serializer = OrderSerializer(order, many=False)

            print(json.dumps(serializer.data, indent=4))

            return Response(serializer.data)


permission_classes([IsAuthenticated])
class OrderDetails(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(_id=pk)
        except Order.DoesNotExist:
            raise Http404

    # get a single order by id for (User, Admin)
    def get(self, request, pk, format=None):
        user = request.user
        order = self.get_object(pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            return Response(
                {'detail':'Not authorized to view this order'},
                status=status.HTTP_401_UNAUTHORIZED
            )

permission_classes([IsAuthenticated])
class UpdateOrderToPaid(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(_id=pk)
        except Order.DoesNotExist:
            raise Http404

    # update order payment status
    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        order.isPaid=True
        order.paidAt = datetime.now()
        order.save()
        return Response({'message': 'Order paid'}, status=status.HTTP_200_OK)


permission_classes([IsAdminUser])
class AdminOrderList(APIView):
    def get(self, request, format=None):
        try:
            orders = Order.objects.all()
            serializer = OrderSerializer(orders, many=True)
        except Order.DoesNotExist:
            raise Http404

        return Response(serializer.data)

permission_classes([IsAdminUser])
class UpdateOrderToDelivered(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(_id=pk)
        except Order.DoesNotExist:
            raise Http404

        # update order payment status
    def put(self, request, pk, format=None):
        order = self.get_object(pk)
        order.isDelivered = True
        order.deliveredAt = datetime.now()
        order.save()
        return Response({'message': 'Order delivered'}, status=status.HTTP_200_OK)
