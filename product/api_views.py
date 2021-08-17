from rest_framework import generics, viewsets
from .models import *
from django.views.decorators.csrf import csrf_exempt
from .serializers import *
from django.http import JsonResponse
from rest_framework import permissions
from .my_permissions import *


# Base View Sets
class BaseApiViewSets(viewsets.ModelViewSet):
    def perform_destroy(self, instance):
        instance.my_delete()


# Category Api View Sets
class CategoryApiViewSets(BaseApiViewSets):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [ISStaffPut]


# Category Short Api View Sets
class CategoryShortApiViewSets(BaseApiViewSets):
    serializer_class = CategoryShortSerializer
    queryset = Category.objects.all()
    permission_classes = [ISStaffPost]


# Discount Api View Sets
class DiscountApiViewSets(BaseApiViewSets):
    serializer_class = DiscountSerializer
    queryset = Discount.objects.all()
    permission_classes = [ISStaffPut]


# Discount Short Api View Sets
class DiscountShortApiViewSets(BaseApiViewSets):
    serializer_class = DiscountShortSerializer
    queryset = Discount.objects.all()
    permission_classes = [ISStaffPost]


# Off Code Api View Sets
class OffCodeApiViewSets(BaseApiViewSets):
    serializer_class = OffCodeSerializer
    queryset = OffCode.objects.all()
    permission_classes = [ISStaffPut]


# Off Code Short Api View Sets
class OffCodeShortApiViewSets(BaseApiViewSets):
    serializer_class = OffCodeShortSerializer
    queryset = OffCode.objects.all()
    permission_classes = [ISStaffPost]


# Brand Api View Sets
class BrandApiViewSets(BaseApiViewSets):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    permission_classes = [ISStaffPut]


# Brand Short Api View Sets
class BrandShortApiViewSets(BaseApiViewSets):
    serializer_class = BrandShortSerializer
    queryset = Brand.objects.all()
    permission_classes = [ISStaffPost]


# Specification Api View Sets
class SpecificationApiViewSets(BaseApiViewSets):
    serializer_class = SpecificationSerializer
    queryset = Specification.objects.all()
    permission_classes = [ISStaffPut]


# Specification Short Api View Sets
class SpecificationShortApiViewSets(BaseApiViewSets):
    serializer_class = SpecificationShortSerializer
    queryset = Specification.objects.all()
    permission_classes = [ISStaffPost]


# Variable Specification Api View Sets
class VariableSpecificationApiViewSets(BaseApiViewSets):
    serializer_class = VariableSpecificationSerializer
    queryset = VariableSpecification.objects.all()
    permission_classes = [ISStaffPut]


# Variable Specification Short Api View Sets
class VariableSpecificationShortApiViewSets(BaseApiViewSets):
    serializer_class = VariableSpecificationShortSerializer
    queryset = VariableSpecification.objects.all()
    permission_classes = [ISStaffPost]


# Menu Item Api View Sets
class MenuItemApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [ISStaffPut]


# Menu Item Short Api View Sets
class MenuItemShortApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemShortSerializer
    queryset = MenuItem.objects.all()
    permission_classes = [ISStaffPost]


# Image Api View Sets
class ImageApiViewSets(BaseApiViewSets):
    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [ISStaffPut]


# Image Short Api View Sets
class ImageShortApiViewSets(BaseApiViewSets):
    serializer_class = ImageShortSerializer
    queryset = Image.objects.all()
    permission_classes = [ISStaffPost]


# Menu item Variant Api View Sets
class MenuItemVariantApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemVariantSerializer
    queryset = MenuItemVariant.objects.all()
    permission_classes = [ISStaffPut]


# Menu item Variant Short Api View Sets
class MenuItemVariantShortApiViewSets(BaseApiViewSets):
    serializer_class = MenuItemVariantShortSerializer
    queryset = MenuItemVariant.objects.all()
    permission_classes = [ISStaffPost]
