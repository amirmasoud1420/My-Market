from rest_framework import permissions
from .models import *


class ISStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class ISStaffObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True


class IsOrderItemOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.order.customer.user == request.user


class IsOrderOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.customer.user == request.user


class OrderStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH']:
            if obj.status in ['c', 'p']:
                return False
        return True


class OrderMenuItemStatus(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.order.status in ['c', 'p']:
                return False
        return True
