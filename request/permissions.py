
from rest_framework.permissions import BasePermission


class CreateRequestOnlyCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == "customer"
        )


class OwnerToSeeAllRequests(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == "admin"
        )


class SingleRequestPermisiion(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.user.role == "admin":
            return True

        if request.user.role == "customer" and obj.customer == request.user:
            return True

        if request.user.role == "provider" and obj.provider and obj.provider.user == request.user:
            return True

        return False
class CancelRequestPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.customer==request.user
class AvailableRequestPermission(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return (
            user.is_authenticated and
            user.role in ['provider' , 'admin']
        )
class AcceptRequestPermission(BasePermission):
    def has_permission(self, request, view):
        user=request.user
        return (
            user.is_authenticated and
            user.role =='provider' 
        )       

class ProviderCurrentJobsPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.role == "provider"