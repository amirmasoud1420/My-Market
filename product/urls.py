from django.urls import path, include
from .views import *

urlpatterns = [
    path('', test, name='test'),
    path('menu-item-card/<int:pk>/', MenuItemCardView.as_view(), name='menu_item_card'),
    path('category/<int:pk>/', MenuItemCategoryView.as_view(), name='menu_item_category'),
    path('detail/<int:pk>/', MenuItemVariantDetailView.as_view(), name='menu_item_detail'),
    path('like/<int:pk>/', MenuItemVariantLikeView.as_view(), name='menu_item_like'),
    path('unlike/<int:pk>/', MenuItemVariantUnLikeView.as_view(), name='menu_item_unlike'),
    path('comment/<int:pk>/', MenuItemCommentView.as_view(), name='menu_item_comment'),
    path('comment-reply/<int:pk>/<int:comment_id>/', MenuItemCommentReplyView.as_view(), name='menu_item_comment_reply'),
]
