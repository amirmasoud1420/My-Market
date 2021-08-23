from django.urls import path

from .views import *

app_name = 'order'
urlpatterns = [
    path('', OrderDetailView.as_view(), name='order_detail'),
    path('paid/', PaidOrderDetailView.as_view(), name='paid_order_detail'),
    path('canceled/', CanceledOrderDetailView.as_view(), name='canceled_order_detail'),
    path('add/<int:pk>/', OrderAddView.as_view(), name='order_add'),
    path('add-off-code/', OffCodeAddView.as_view(), name='off_code_add'),
    path('add-quantity/<int:pk>/', AddQuantityView.as_view(), name='add_quantity'),
    path('remove-quantity/<int:pk>/', RemoveQuantityView.as_view(), name='remove_quantity'),
    path('delete-order-item/<int:pk>/', RemoveOrderItemView.as_view(), name='remove_order_item'),
    path('create-order/<int:pk>/', CreateOrderView.as_view(), name='create_order'),
    path('remove-off-code/<int:pk>/', RemoveOffCodeView.as_view(), name='remove_off_code'),
    path('select-address/', SelectAddress.as_view(), name='select_address'),
    path('add-address/', AddressCreateView.as_view(), name='add_address'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('cancel-order/', CancelOrderView.as_view(), name='cancel_order'),
]
