import json
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from product.models import Product
from review.models import Review


# Create your views here.
permission_classes([IsAuthenticated])
class CreateProductReview(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(_id=pk)
        except Product.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        user = request.user
        product= self.get_object(pk)
        data = request.data

        alreadyExist = product.review_set.filter(user=user).exists()

        if alreadyExist:
            content = {'detail': 'Product already reviewed'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        elif data['rating'] == 0:
            content = {'detail': 'please select a rating '}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        else:
            review = Review.objects.create(
                user=user,
                product=product,
                name=user.first_name,
                rating=data['rating'],
                comment=data['comment']
            )

            reviews = product.review_set.all()
            product.numReview = len(reviews)

            sum_of_rating = 0
            for i in reviews:
                sum_of_rating += i.rating

            product.rating = sum_of_rating / product.numReview
            product.save()

            return Response({'detail': 'Review added'}, status=status.HTTP_201_CREATED)





