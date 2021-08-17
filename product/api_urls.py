from django.urls import path, include
from .api_views import *

urlpatterns = [
    # category
    path('category-list/', CategoryShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='category_list_api'),
    path('category-detail/<int:pk>', CategoryApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='category_detail_api'),

    # discount
    path('discount-list/', DiscountShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='discount_list_api'),
    path('discount-detail/<int:pk>', DiscountApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='discount_detail_api'),

    # off code
    path('offcode-list/', OffCodeShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='offcode_list_api'),
    path('offcode-detail/<int:pk>', OffCodeApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='offcode_detail_api'),

    # brand
    path('brand-list/', BrandShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='brand_list_api'),
    path('brand-detail/<int:pk>', BrandApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='brand_detail_api'),

    # specification
    path('specification-list/', SpecificationShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='specification_list_api'),
    path('specification-detail/<int:pk>', SpecificationApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='specification_detail_api'),

    # variable specification
    path('variable-specification-list/', VariableSpecificationShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='variable_specification_list_api'),
    path('variable-specification-detail/<int:pk>', VariableSpecificationApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='variable_specification_detail_api'),

    # menu item
    path('menu-item-list/', MenuItemShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='menu_item_list_api'),
    path('menu-item-detail/<int:pk>', MenuItemApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='menu_item_detail_api'),

    # image
    path('image-list/', ImageShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='image_list_api'),
    path('image-detail/<int:pk>', ImageApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='image_detail_api'),

    # menu item variant
    path('menu-item-variant-list/', MenuItemVariantShortApiViewSets.as_view(
        {
            'get': 'list',
            'post': 'create',
        }), name='menu_item_variant_list_api'),
    path('menu-item-variant-detail/<int:pk>', MenuItemVariantApiViewSets.as_view(
        {
            'get': 'retrieve',
            'put': 'update',
            'patch': 'partial_update',
            'delete': 'destroy',
        }), name='menu_item_variant_detail_api'),

]
