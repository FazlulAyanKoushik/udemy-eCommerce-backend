import json
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from product.models import Product
from product.serializers import ProductSerializer, ProductUpdateSerializer

# Create your views here.
@api_view(['GET'])
def get_products(request):
    """
    List all Products.
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product_by_id(request, id):
    """
    Get Product By ID
    """
    product = Product.objects.get(_id= id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def createProduct(request):
    user = request.user

    product = Product.objects.create(
        seller=user,
        name='Sample Name',
        price=0,
        brand='Sample Brand',
        countInStock=0,
        category='Sample Category',
        description=''
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)




# Class Based Views
# @permission_classes([IsAuthenticated])
class ProductList(APIView):
    """
    List all Products, or create a new Product.
    """
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]
    def get(self, request, format=None):
        query = request.query_params.get('keyword')
        if query is None:
            query = ''

        products = Product.objects.filter(name__icontains=query)

        # Pagination
        page = request.query_params.get('page')
        paginator = Paginator(products, 2)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        serializer = ProductSerializer(products, many=True)
        return Response({
            'products': serializer.data,
            'page':page,
            'pages':paginator.num_pages
        })


    permission_classes([IsAdminUser])
    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(seller=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTopProducts(APIView):
    def get(self, request, format=None):
        query = request.query_params.get('keyword')
        if query is None:
            query = ''
        products = Product.objects.filter(rating__gte=4, name__icontains=query).order_by('-rating')[:5]

        # Pagination
        page = request.query_params.get('page')
        paginator = Paginator(products, 10)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)

        if page is None:
            page = 1

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)
        # return Response({
        #     'products': serializer.data,
        #     'page': page,
        #     'pages': paginator.num_pages
        # })


class ProductDetail(APIView):
    """
    Retrieve, update or delete a Product instance.
    """
    def get_object(self, id):
        try:
            return Product.objects.get(_id=id)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    permission_classes([IsAdminUser])
    def put(self, request, id, format=None):
        product = self.get_object(id)
        serializer = ProductUpdateSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    permission_classes([IsAdminUser])
    def delete(self, request, id, format=None):
        product = self.get_object(id)
        product.delete()
        return Response("Product Deleted successfully")


@api_view(['POST'])
def uploadImage(request):
    data = request.data
    product_id = data['product_id']
    try:
        product = Product.objects.get(_id=product_id)
        product.image = request.FILES.get('image')
        product.save()
        return Response('Image was uploaded')
    except:
        return Response('Image upload fail')
