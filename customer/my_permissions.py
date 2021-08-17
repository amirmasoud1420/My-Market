from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner.user == request.user


class ISStaffListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True


class IsCustomer(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            if request.user.is_staff:
                return True
        if request.method == 'POST':
            return True


class ISStaffObj(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
