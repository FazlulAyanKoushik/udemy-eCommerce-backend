from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getRoutes, name="base"),
    path('get-products/', views.getProducts, name="get-products"),
    path('get-product/<str:pk>/', views.getProductByID, name="get-product"),
    
]