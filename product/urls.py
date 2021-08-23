from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='product_home'),
    path('menu-item-card/<int:pk>/', MenuItemCardView.as_view(), name='menu_item_card'),
    path('category/<int:pk>/', MenuItemCategoryView.as_view(), name='menu_item_category'),
    path('detail/<int:pk>/', MenuItemVariantDetailView.as_view(), name='menu_item_detail'),
    path('like/<int:pk>/', MenuItemVariantLikeView.as_view(), name='menu_item_like'),
    path('unlike/<int:pk>/', MenuItemVariantUnLikeView.as_view(), name='menu_item_unlike'),
    path('comment/<int:pk>/', MenuItemCommentView.as_view(), name='menu_item_comment'),
    path('comment-reply/<int:pk>/<int:comment_id>/', MenuItemCommentReplyView.as_view(),
         name='menu_item_comment_reply'),
    path('comment-like/<int:pk>/', CommentLikeView.as_view(), name='comment_like'),
    path('comment-unlike/<int:pk>/', CommentUnLikeView.as_view(), name='comment_unlike'),
    path('product-serach/', ProductSearchView.as_view(), name='product_search'),
]
