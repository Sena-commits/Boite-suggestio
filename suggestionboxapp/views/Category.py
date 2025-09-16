from rest_framework import generics, permissions
from suggestionboxapp.permissions import IsModeratorOrAdmin
from suggestionboxapp.models import Category 
from suggestionboxapp.serializers import CategorySerializer


class CategoryListView(generics.ListCreateAPIView):
    """Liste et création des catégories"""
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Seuls les admins peuvent créer des catégories
        if not self.request.user.role == 'admin':
            raise permissions.PermissionDenied("Seuls les administrateurs peuvent créer des catégories")
        serializer.save()

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression de catégorie"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsModeratorOrAdmin]
