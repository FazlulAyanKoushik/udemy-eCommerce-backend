from django.urls import path
from . import views

urlpatterns = [
    path('<str:pk>/', views.CreateProductReview.as_view(), name='add-review')
]