from rest_framework import serializers
from .models import *


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = '__all__'
        depth = 5


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer()
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # brand = BrandSerializer()
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    # specifications = SpecificationSerializer(many=True)
    specifications = serializers.PrimaryKeyRelatedField(queryset=Specification.objects.all(), many=True)

    class Meta:
        model = MenuItem
        fields = '__all__'
        depth = 5


class VariableSpecificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableSpecification
        fields = '__all__'


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class MenuItemVariantSerializer(serializers.ModelSerializer):
    # menu_item = MenuItemSerializer()
    menu_item = serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    # variable_specifications = VariableSpecificationsSerializer( many=True)
    variable_specifications = serializers.PrimaryKeyRelatedField(queryset=VariableSpecification.objects.all(),
                                                                 many=True)
    # discount = DiscountSerializer()
    discount = serializers.PrimaryKeyRelatedField(queryset=Discount.objects.all())

    class Meta:
        model = MenuItemVariant
        fields = '__all__'
        read_only_fields = ['id', 'create_time_stamp', 'modify_time_stamp', 'delete_time_stamp', 'is_deleted']
        depth = 5
