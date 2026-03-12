from rest_framework.permissions import BasePermission

class CustomerProfilePermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == "POST":
            return (
                request.user and
                request.user.is_authenticated and
                request.user.role == "customer"
            )

        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PATCH", "POST","DELETE"]:
            return obj.user == request.user
        return False    
class ProviderProfilePermission(BasePermission):
    def has_permission(self, request, view):

        if request.method == "POST":
            return (
                request.user and
                request.user.is_authenticated and
                request.user.role == "provider"
            )

        return request.user and request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        if request.method in ["GET", "PATCH", "POST","DELETE"]:
            return obj.user == request.user
        return False        