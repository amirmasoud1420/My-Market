from rest_framework import permissions
from .models import *


class ISStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class ISStaffPost(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            if request.user.is_staff:
                return True


class ISStaffPut(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if request.user.is_staff:
                return True
