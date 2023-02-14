from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('user/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('users/register/', views.registerUser, name='users-register'), # Function Based

    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('refresh/', views.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # path('users/profile/', views.getUserProfile, name="users-profile"), # Function Based
    path('user/profile/', views.UserProfileView.as_view(), name="user-profile"),

    # path('users/update/profile/', views.updateUserProfile, name="update-profile"), # Function Based (update-user)
    path('user/update/profile/', views.UserProfileDetails.as_view(), name="user-update-profile"), # (update-user)

    path('get-users/', views.getAllUserProfile, name="get-users"), # Function Based  (Admin- users,)
    path('users/', views.AllUserProfileView.as_view(), name="all-users"), #(Admin- users,)
    path('user/<str:pk>/', views.GetUserByAdminView.as_view(), name="get-user-by-id"), #(Admin- users,)
    path('user/update/<str:pk>/', views.GetUserByAdminView.as_view(), name="update-user-by-id"), #(Admin- users,)
    path('user/delete/<str:pk>/', views.GetUserByAdminView.as_view(), name="delete-user"), #(Admin- users,)

    # path('user/<str:pk>/', views.getUserById, name="get-user")
]