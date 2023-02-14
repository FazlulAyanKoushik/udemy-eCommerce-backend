from django.urls import path, include
from . import views

urlpatterns = [
    # function based views
    path('get-products/', views.get_products, name="get-products"),
    path('get-product/<str:id>/', views.get_product_by_id, name="get-product"),
    path('product/create/', views.createProduct, name="product-create"),
    path('product/upload/', views.uploadImage, name="image-upload"),


    # class based views
    path('products/', views.ProductList.as_view()),
    path('products/top/', views.GetTopProducts.as_view()),
    path('product/<str:id>/', views.ProductDetail.as_view(), name="get-product-by-id"),

    # Only Admin Access
    path('products/add/', views.ProductList.as_view()),
    path('product/update/<str:id>/', views.ProductDetail.as_view(), name="delete-product-by-id"),
    path('product/delete/<str:id>/', views.ProductDetail.as_view(), name="delete-product-by-id"),


]