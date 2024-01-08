from rest_framework import permissions


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.paypal_email)


class IsAttachOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.product_owner == request.user or request.user.is_staff
