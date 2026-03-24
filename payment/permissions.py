from rest_framework.permissions import BasePermission


# only Customer can access and evrey customer can access their own endpoint
class IsCustomerAndOwner(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "customer"

    def has_object_permission(self, request, view, obj):
        return obj.servicerequest.customer == request.user
    
# only provider can access and evrey custprovideromer can access their own endpoint
class IsProviderOnly(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "provider"

    def has_object_permission(self, request, view, obj):
        return obj.servicerequest.customer == request.user    
    
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


