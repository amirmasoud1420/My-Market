from django.shortcuts import render

# Create your views here.
from django.views import View, generic

from .models import *


def test(request):
    return render(request, 'base/base.html')


class MenuItemCardView(generic.DetailView):
    template_name = 'menu_item/menu_item_card.html'
    model = MenuItemVariant
    context_object_name = 'menu_item'


class MenuItemCategoryView(generic.DetailView):
    template_name = 'menu_item/menu_item_list.html'
    model = Category
    context_object_name = 'category'


class MenuItemVariantDetailView(generic.DetailView):
    template_name = 'menu_item/menu_item_detail.html'
    model = MenuItemVariant
    context_object_name = 'menu_item_variant'
