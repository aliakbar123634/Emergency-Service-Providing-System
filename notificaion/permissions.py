from rest_framework.permissions import BasePermission


class AdminOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        
        print("USER:", request.user)
        print("ROLE:", getattr(request.user, "role", None))
        user=request.user
        return user.is_authenticated and user.role=="admin"