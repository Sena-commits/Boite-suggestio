from rest_framework import permissions



class IsModeratorOrAdmin(permissions.BasePermission):
    """Permission pour les modérateurs et administrateurs"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_moderator_or_admin
        )