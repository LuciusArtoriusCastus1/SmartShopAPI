from rest_framework import permissions


class IsMemberOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.members in [request.user] or request.user.is_staff
