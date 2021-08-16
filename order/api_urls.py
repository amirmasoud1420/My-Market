from django.urls import path, include
from .api_views import *

urlpatterns = [
    # order
    path('order-list/', OrderShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='order_list_api'),
    path('order-detail/<int:pk>', OrderApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
        }), name='order_detail_api'),

    # order menu item
    path('order-menu-item-list/', OrderMenuItemShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='order_menu_item_list_api'),
    path('order-menu-item-detail/<int:pk>', OrderMenuItemApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='order_menu_item_detail_api'),
]
