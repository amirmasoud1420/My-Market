from django.contrib import admin

# Register your models here.
from .models import *


class BaseAdmin(admin.ModelAdmin):
    exclude = ['delete_time_stamp']


admin.site.register(Category, BaseAdmin)
admin.site.register(Discount, BaseAdmin)
admin.site.register(OffCode, BaseAdmin)
admin.site.register(Brand, BaseAdmin)
admin.site.register(Image, BaseAdmin)
admin.site.register(Specification, BaseAdmin)
admin.site.register(VariableSpecification, BaseAdmin)
admin.site.register(MenuItem, BaseAdmin)
admin.site.register(MenuItemVariant, BaseAdmin)
