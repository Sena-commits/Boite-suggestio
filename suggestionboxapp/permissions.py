from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission personnalisée pour permettre seulement aux propriétaires d'éditer leurs objets.
    """
    
    def has_object_permission(self, request, view, obj):
        # Permissions de lecture pour tous
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissions d'écriture seulement pour le propriétaire
        if hasattr(obj, 'author'):
            return obj.author == request.user
        
        return False

class IsModeratorOrAdmin(permissions.BasePermission):
    """Permission pour les modérateurs et administrateurs"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.is_moderator_or_admin
        )

class IsAdminOnly(permissions.BasePermission):
    """Permission pour les administrateurs uniquement"""
    
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.role == 'admin'
        )

class CanModifyStatus(permissions.BasePermission):
    """Permission pour modifier le statut des suggestions"""
    
    def has_permission(self, request, view):
        # Seuls les modérateurs et admins peuvent changer les statuts
        return (
            request.user.is_authenticated and
            request.user.is_moderator_or_admin
        )