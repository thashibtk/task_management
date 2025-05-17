from rest_framework import permissions

class IsSuperAdminOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.role in ['superadmin', 'admin']