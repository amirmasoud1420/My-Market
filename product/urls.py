from django.urls import path, include
from .views import *
from .api_views import *

urlpatterns = [
    path('', test, name='test'),
    path('menu-item-card/<int:pk>/', MenuItemCardView.as_view(), name='menu_item_card'),
    path('menu-item-category/<int:pk>/', MenuItemCategoryView.as_view(), name='menu_item_category'),
    path('menu-item-detail/<int:pk>/', MenuItemVariantDetailView.as_view(), name='menu_item_detail'),

    path('menu-item-api/', ProductApiView, name='product_api'),
    path('menu-item-list-api/', ProductListApiView.as_view(), name='menu_item_list_api'),
    path('menu-item-detail-api/<int:pk>', ProductDetailView.as_view(), name='menu_item_detail_api'),
]
