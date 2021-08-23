from django.contrib import admin
from .models import *


# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'final_price')


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'menu_item_variant', 'quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderMenuItem, OrderItemAdmin)
