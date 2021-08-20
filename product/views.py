from django.shortcuts import render, redirect

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

    def get(self, request, *args, **kwargs):
        menu_item_variant = MenuItemVariant.objects.get(id=kwargs['pk'])
        variants = menu_item_variant.menu_item.menuitemvariant_set.all()
        # default_variant = variants[0]
        context = {
            'menu_item_variant': menu_item_variant,
            'variants': variants,
            # 'default_variant': default_variant,
        }
        return render(request, 'menu_item/menu_item_detail.html', context)
        # super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        menu_item_variant = MenuItemVariant.objects.get(id=request.POST.get('select'))
        variants = menu_item_variant.menu_item.menuitemvariant_set.all()
        context = {
            'menu_item_variant': menu_item_variant,
            'variants': variants,
            # 'default_variant': default_variant,
        }
        return redirect('menu_item_detail', pk=request.POST.get('select'))
        # return render(request, 'menu_item/menu_item_detail.html', context)
