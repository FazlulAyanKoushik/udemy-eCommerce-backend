from django.urls import path
from . import views

urlpatterns = [
    # path('add/', views.addOrder, name='add-order'),
    path('add/', views.OrderList.as_view(), name='add-order'),
    path('user/list/', views.OrderList.as_view(), name='list-order'),
    path('details/<str:pk>/', views.OrderDetails.as_view(), name='get-order-by-id'),
    path('<str:pk>/pay/', views.UpdateOrderToPaid.as_view(), name='order-to-paid'),

    path('lists/', views.AdminOrderList.as_view(), name='list-order'),
    path('<str:pk>/deliver/', views.UpdateOrderToDelivered.as_view(), name='deliver-order'),

]