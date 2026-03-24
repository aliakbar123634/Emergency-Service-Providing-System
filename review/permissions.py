from rest_framework.permissions import BasePermission

class IsCustomerOnly(BasePermission):
    message = "Only customers can perform this action."

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'customer'
    
#   Every Customer can access its own reviews    
class OnlyCustomerAndOwnAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'customer'
    def has_object_permission(self, request, view, obj):
        obj.user=request.user.customer   


class OnlyProviderAndOwnAccess(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'provider'
    def has_object_permission(self, request, view, obj):
        obj.user=request.user.provider  


class OnlyCustomerOwnAccessAndOwner(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role_in == [ 'customer' , 'admin']
    def has_object_permission(self, request, view, obj):
        obj.user=request.user.customer          