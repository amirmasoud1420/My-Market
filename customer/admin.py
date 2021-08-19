from django.contrib import admin
from .models import *


# Register your models here.
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user']


class AddressAdmin(admin.ModelAdmin):
    list_display = ['owner', 'state', 'city']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address,AddressAdmin)
