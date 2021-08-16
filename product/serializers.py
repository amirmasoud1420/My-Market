from rest_framework import serializers
from .models import *
from .api_views import *


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(view_name='category_detail_api', queryset=Category.objects.all(),
                                                 required=False, allow_null=True)
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = '__all__'


# Category Short Serializer
class CategoryShortSerializer(serializers.ModelSerializer):
    parent = serializers.HyperlinkedRelatedField(view_name='category_detail_api', queryset=Category.objects.all(),
                                                 required=False, allow_null=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']


# Discount Serializer
class DiscountSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Discount
        fields = '__all__'


# Discount Short Serializer
class DiscountShortSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = Discount
        fields = ['id', 'is_percent', 'price', 'percent', 'max', 'expire_date_time', 'is_expired']


# Off Code Serializer
class OffCodeSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = OffCode
        fields = '__all__'


# Off Code Short Serializer
class OffCodeShortSerializer(serializers.ModelSerializer):
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = OffCode
        fields = ['id', 'is_percent', 'price', 'percent', 'max', 'expire_date_time', 'is_expired', 'code']


# Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Brand
        fields = '__all__'


# Brand Short Serializer
class BrandShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name']


# Specification Serializer
class SpecificationSerializer(serializers.ModelSerializer):
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Specification
        fields = '__all__'


# Specification Short Serializer
class SpecificationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification
        fields = ['id', 'name', 'value']


# Variable Specification Serializer
class VariableSpecificationSerializer(serializers.ModelSerializer):
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = VariableSpecification
        fields = '__all__'


# Variable Specification Short Serializer
class VariableSpecificationShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariableSpecification
        fields = ['id', 'name', 'value']


# Image Serializer
class ImageSerializer(serializers.ModelSerializer):
    menu_item = serializers.HyperlinkedRelatedField(view_name='menu_item_detail_api', queryset=MenuItem.objects.all())
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = Image
        fields = '__all__'


# Image Short Serializer
class ImageShortSerializer(serializers.ModelSerializer):
    menu_item = serializers.HyperlinkedRelatedField(view_name='menu_item_detail_api', queryset=MenuItem.objects.all())

    class Meta:
        model = Image
        fields = ['id', 'image', 'menu_item']


# Menu Item Serializer
class MenuItemSerializer(serializers.ModelSerializer):
    brand = serializers.HyperlinkedRelatedField(view_name='brand_detail_api', queryset=Brand.objects.all())
    category = serializers.HyperlinkedRelatedField(view_name='category_detail_api', queryset=Category.objects.all())
    specifications = serializers.HyperlinkedRelatedField(view_name='specification_detail_api',
                                                         queryset=Specification.objects.all(), many=True)
    images = serializers.HyperlinkedRelatedField(view_name='image_detail_api', queryset=Image.objects.all(),
                                                 source='image_set', many=True)
    menu_item_variants = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api',
                                                             queryset=MenuItemVariant.objects.all(), many=True,
                                                             source='menuitemvariant_set')
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = MenuItem
        fields = '__all__'


# Menu Item Short Serializer
class MenuItemShortSerializer(serializers.ModelSerializer):
    brand = serializers.HyperlinkedRelatedField(view_name='brand_detail_api', queryset=Brand.objects.all())
    category = serializers.HyperlinkedRelatedField(view_name='category_detail_api', queryset=Category.objects.all())
    specifications = serializers.HyperlinkedRelatedField(view_name='specification_detail_api',
                                                         queryset=Specification.objects.all(), many=True)
    images = serializers.HyperlinkedRelatedField(view_name='image_detail_api', queryset=Image.objects.all(),
                                                 source='image_set', many=True)
    menu_item_variants = serializers.HyperlinkedRelatedField(view_name='menu_item_variant_detail_api',
                                                             queryset=MenuItemVariant.objects.all(), many=True,
                                                             source='menuitemvariant_set')

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'category', 'brand', 'specifications', 'description', 'images', 'menu_item_variants']


# Menu Item Variant Serializer
class MenuItemVariantSerializer(serializers.ModelSerializer):
    menu_item = serializers.HyperlinkedRelatedField(view_name='menu_item_detail_api', queryset=MenuItem.objects.all())
    variable_specifications = serializers.HyperlinkedRelatedField(view_name='variable_specification_detail_api',
                                                                  queryset=VariableSpecification.objects.all(),
                                                                  many=True)
    discount = serializers.HyperlinkedRelatedField(view_name='discount_detail_api', queryset=Discount.objects.all())
    final_price = serializers.ReadOnlyField()
    is_deleted = serializers.ReadOnlyField()
    delete_time_stamp = serializers.ReadOnlyField()

    class Meta:
        model = MenuItemVariant
        fields = '__all__'


# Menu Item Variant Short Serializer
class MenuItemVariantShortSerializer(serializers.ModelSerializer):
    menu_item = serializers.HyperlinkedRelatedField(view_name='menu_item_detail_api', queryset=MenuItem.objects.all())
    variable_specifications = serializers.HyperlinkedRelatedField(view_name='variable_specification_detail_api',
                                                                  queryset=VariableSpecification.objects.all(),
                                                                  many=True)
    discount = serializers.HyperlinkedRelatedField(view_name='discount_detail_api', queryset=Discount.objects.all(),
                                                   required=False, allow_null=True)
    final_price = serializers.ReadOnlyField()

    class Meta:
        model = MenuItemVariant
        fields = ['id', 'menu_item', 'variable_specifications', 'price', 'count', 'discount', 'final_price']
