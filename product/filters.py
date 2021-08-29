import django_filters
from django import forms
from .models import *
from django.utils.translation import gettext_lazy as _


class MenuItemVariantFilter(django_filters.FilterSet):
    choice_1 = {
        (_('highest price'), 'highest price'),
        (_('lowest price'), 'lowest price'),
    }
    choice_2 = {
        (_('oldest'), 'oldest'),
        (_('newest'), 'newest'),
    }
    choice_3 = {
        (_('most discount'), 'most discount'),
        (_('lowest discount'), 'lowest discount'),
    }
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price = django_filters.ChoiceFilter(choices=choice_1, method='price_filter')
    create_time_stamp = django_filters.ChoiceFilter(choices=choice_2, method='create_filter')
    discount = django_filters.ChoiceFilter(choices=choice_3, method='discount_filter')

    def create_filter(self, queryset, name, value):
        create_field = 'create_time_stamp' if value == 'oldest' else '-create_time_stamp'
        return queryset.order_by(create_field)

    def price_filter(self, queryset, name, value):
        order_field = 'price' if value == 'lowest price' else '-price'
        return queryset.order_by(order_field)

    def discount_filter(self, queryset, name, value):
        order_field = '-discount__percent' if value == 'most discount' else 'discount__percent'
        return queryset.order_by(order_field)


class MenuItemFilter(django_filters.FilterSet):
    choice_1 = {
        (_('bestselling'), 'bestselling'),
        (_('lowest sales'), 'lowest sales'),
    }
    brand = django_filters.ModelMultipleChoiceFilter(
        queryset=Brand.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
    sell = django_filters.ChoiceFilter(choices=choice_1, method='sell_filter')

    def sell_filter(self, queryset, name, value):
        order_field = '-sell' if value == 'bestselling' else 'sell'
        return queryset.order_by(order_field)
