from django.contrib import admin

# Register your models here.
from .models import *


class BaseAdmin(admin.ModelAdmin):
    exclude = ['delete_time_stamp']


class MenuItemVariantInlines(admin.TabularInline):
    model = MenuItemVariant
    extra = 1


class CategoryAdmin(BaseAdmin):
    list_display = ('name', 'create_time_stamp', 'modify_time_stamp')


class MenuItemAdmin(BaseAdmin):
    list_display = ('name', 'create_time_stamp', 'modify_time_stamp')
    inlines = [MenuItemVariantInlines]


class MenuItemVariantAdmin(BaseAdmin):
    list_display = ('menu_item', 'count', 'price', 'final_price')
    list_editable = ('count', 'price')


class CommentAdmin(BaseAdmin):
    list_display = ('user', 'create_time_stamp', 'rate')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Discount, BaseAdmin)
admin.site.register(OffCode, BaseAdmin)
admin.site.register(Brand, BaseAdmin)
admin.site.register(Image, BaseAdmin)
admin.site.register(Specification, BaseAdmin)
admin.site.register(VariableSpecification, BaseAdmin)
admin.site.register(MenuItem, MenuItemAdmin)
admin.site.register(MenuItemVariant, MenuItemVariantAdmin)
admin.site.register(Comment, CommentAdmin)
