from django.urls import path

from .views import *

app_name = 'customer'
urlpatterns = [
    path('register/', CustomerRegisterView.as_view(), name='customer_register'),
    path('login/', CustomerLoginView.as_view(), name='customer_login'),
    path('logout/', CustomerLogoutView.as_view(), name='customer_logout'),
    path('profile/', CustomerProfileView.as_view(), name='customer_profile'),
    path('profile/update/', CustomerProfileUpdateView.as_view(), name='customer_profile_update'),
    path('add-address/', AddressCreateView.as_view(), name='add_address'),
    path('update-address/<int:pk>/', AddressUpdateView.as_view(), name='update_address'),
    path('delete-address/<int:pk>/', AddressDeleteView.as_view(), name='delete_address'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('favorites/', FavoritesView.as_view(), name='favorites'),
]
