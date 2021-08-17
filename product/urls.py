from django.urls import path, include
from .views import *


urlpatterns = [
    path('', test, name='test'),
    path('menu-item-card/<int:pk>/', MenuItemCardView.as_view(), name='menu_item_card'),
    path('menu-item-category/<int:pk>/', MenuItemCategoryView.as_view(), name='menu_item_category'),
    path('menu-item-detail/<int:pk>/', MenuItemVariantDetailView.as_view(), name='menu_item_detail'),
]
