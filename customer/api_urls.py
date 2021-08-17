from django.urls import path, include
from .api_views import *

urlpatterns = [
    # user
    path('user-list/', UserShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='user_list_api'),
    path('user-detail/<int:pk>', UserApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='user_detail_api'),

    # customer
    path('customer-list/', CustomerShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='customer_list_api'),
    path('customer-list-admin/', CustomerListAdminApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='customer_list_admin_api'),
    path('customer-detail/<int:pk>', CustomerApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='customer_detail_api'),

    # address
    path('address-list/', AddressListForCustomerApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='address_list_api'),
    path('address-detail/<int:pk>', AddressApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='address_detail_api'),
    path('address-list-admin/', AddressShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='address_list_admin_api'),
]
