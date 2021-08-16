from rest_framework import generics, viewsets
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from django.http import JsonResponse


# Base View Sets
class BaseApiViewSets(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        instance.my_delete()


# Category Api View Sets
class CategoryApiViewSets(BaseApiViewSets):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


# Category Short Api View Sets
class CategoryShortApiViewSets(BaseApiViewSets):
    serializer_class = CategoryShortSerializer
    queryset = Category.objects.all()


# Discount Api View Sets
class DiscountApiViewSets(BaseApiViewSets):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()


# Discount Short Api View Sets
class DiscountShortApiViewSets(BaseApiViewSets):
    serializer_class = DiscountShortSerializer
    queryset = Discount.objects.all()


# Off Code Api View Sets
class OffCodeApiViewSets(BaseApiViewSets):
    serializer_class = OffCodeSerializer
    queryset = OffCode.objects.all()


# Off Code Short Api View Sets
class OffCodeShortApiViewSets(BaseApiViewSets):
    serializer_class = OffCodeShortSerializer
    queryset = OffCode.objects.all()


# Brand Api View Sets
class BrandApiViewSets(BaseApiViewSets):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


# Brand Short Api View Sets
class BrandShortApiViewSets(BaseApiViewSets):
    serializer_class = BrandShortSerializer
    queryset = Brand.objects.all()


# Specification Api View Sets
class SpecificationApiViewSets(BaseApiViewSets):
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()


# Specification Short Api View Sets
class SpecificationShortApiViewSets(BaseApiViewSets):
    serializer_class = SpecificationShortSerializer
    queryset = Specification.objects.all()


# Variable Specification Api View Sets
class VariableSpecificationApiViewSets(BaseApiViewSets):
    serializer_class = VariableSpecificationSerializer
    queryset = VariableSpecification.objects.all()


# Variable Specification Short Api View Sets
class VariableSpecificationShortApiViewSets(BaseApiViewSets):
    serializer_class = VariableSpecificationShortSerializer
    queryset = VariableSpecification.objects.all()


# Menu Item Api View Sets
class MenuItemApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()


# Menu Item Short Api View Sets
class MenuItemShortApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemShortSerializer
    queryset = MenuItem.objects.all()


# Image Api View Sets
class ImageApiViewSets(BaseApiViewSets):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()


# Image Short Api View Sets
class ImageShortApiViewSets(BaseApiViewSets):
    serializer_class = ImageShortSerializer
    queryset = Image.objects.all()


# Menu item Variant Api View Sets
class MenuItemVariantApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemVariantSerializer
    queryset = MenuItemVariant.objects.all()


# Menu item Variant Short Api View Sets
class MenuItemVariantShortApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemVariantShortSerializer
    queryset = MenuItemVariant.objects.all()
