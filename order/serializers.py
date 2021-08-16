from rest_framework import serializers
from rest_framework.response import Response

from .models import *
from product.models import *
from customer.models import *


# Order Serializer
class OrderSerializer(serializers.ModelSerializer):
    pure_price = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()
    order_menu_items = serializers.HyperlinkedRelatedField(view_name='order_menu_item_detail_api',
                                                           read_only=True,
                                                           many=True, source='ordermenuitem_set')
    menu_item_variants = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api',
                                                             many=True, read_only=True)
    customer = serializers.HyperlinkedRelatedField(view_name='customer_detail_api', read_only=True)
    off_code = serializers.HyperlinkedRelatedField(view_name='offcode_detail_api', queryset=OffCode.objects.all())
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Order
        fields = '__all__'


# Order Short Serializer
class OrderShortSerializer(serializers.ModelSerializer):
    pure_price = serializers.ReadOnlyField()
    final_price = serializers.ReadOnlyField()
    order_menu_items = serializers.HyperlinkedRelatedField(view_name='order_menu_item_detail_api',
                                                           queryset=OrderMenuItem.objects.all(),
                                                           many=True, source='ordermenuitem_set')
    menu_item_variants = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api',
                                                             many=True, read_only=True)
    customer = serializers.HyperlinkedRelatedField(view_name='customer_detail_api', queryset=Customer.objects.all())
    off_code = serializers.HyperlinkedRelatedField(view_name='offcode_detail_api', queryset=OffCode.objects.all())

    class Meta:
        model = Order
        fields = ['id', 'customer', 'off_code', 'status', 'menu_item_variants', 'pure_price', 'final_price',
                  'order_menu_items']


# Order Menu Item Serializer
class OrderMenuItemSerializer(serializers.ModelSerializer):
    menu_item_variant = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api', read_only=True)
    order = serializers.HyperlinkedRelatedField(view_name='order_detail_api', read_only=True)
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = OrderMenuItem
        fields = '__all__'


# Order Menu Item Short Serializer
class OrderMenuItemShortSerializer(serializers.ModelSerializer):
    menu_item_variant = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api',
                                                            queryset=MenuItemVariant.objects.all())
    order = serializers.HyperlinkedRelatedField(view_name='order_detail_api', queryset=Order.objects.all())

    class Meta:
        model = OrderMenuItem
        fields = ['id', 'order', 'menu_item_variant', 'quantity']
