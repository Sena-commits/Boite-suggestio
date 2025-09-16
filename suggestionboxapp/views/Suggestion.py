from rest_framework import generics
from rest_framework.response import Response
from django.db.models import F

from suggestionboxapp.models import Suggestion
from suggestionboxapp.serializers.SuggestionSerializer import  SuggestionListSerializer, SuggestionDetailSerializer

from suggestionboxapp.permissions import IsOwnerOrReadOnly



class SuggestionListCreateView(generics.ListCreateAPIView):
    """Liste et création des suggestions"""
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return SuggestionDetailSerializer
        return SuggestionListSerializer
    
    def get_queryset(self):
        queryset = Suggestion.objects.select_related('author', 'category').prefetch_related('votes')
        
        # Filtrage par paramètres
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
            
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
            
        is_anonymous = self.request.query_params.get('is_anonymous')
        if is_anonymous is not None:
            queryset = queryset.filter(is_anonymous=is_anonymous.lower() == 'true')
        
        # Recherche
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(description__icontains=search)
        
        # Tri
        ordering = self.request.query_params.get('ordering', '-created_at')
        queryset = queryset.order_by(ordering)
        
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class SuggestionDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Détail, modification et suppression de suggestion"""
    queryset = Suggestion.objects.select_related('author', 'category', 'assigned_to').prefetch_related('comments__author')
    serializer_class = SuggestionDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        # Incrémenter le compteur de vues
        instance = self.get_object()
        instance.views_count = F('views_count') + 1
        instance.save(update_fields=['views_count'])
        instance.refresh_from_db()
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
