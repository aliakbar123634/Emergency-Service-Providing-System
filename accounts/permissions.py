from rest_framework.permissions import BasePermission


class onlyUserpermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj==request.user
    
class AdminOnlyPermission(BasePermission):
    
    def has_permission(self, request, view):
        user=request.user
        return (
            user and
            user.is_authenticated and
            user.role=='admin'
        )    