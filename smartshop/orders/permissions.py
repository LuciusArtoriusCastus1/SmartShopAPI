from rest_framework import permissions


class IsOwnerCustomerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(not (obj.paid_up or obj.declined), 'sdfhgsdklhfgsjdkgdskljgfsdhfgkdjfhgkdshgfl')
        if request.method in permissions.SAFE_METHODS:
            return request.user in (obj.product.owner, obj.customer) or request.user.is_staff
        return not (obj.paid_up or obj.declined)
