from rest_framework import  status 
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from suggestionboxapp.models import  Suggestion, Comment
from suggestionboxapp.serializers import  CommentSerializer




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, pk):
    """Ajouter un commentaire à une suggestion"""
    suggestion = get_object_or_404(Suggestion, pk=pk)
    
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        # Vérifier si c'est une réponse à un autre commentaire
        parent_id = request.data.get('parent')
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, pk=parent_id, suggestion=suggestion)
        
        comment = serializer.save(
            author=request.user, 
            suggestion=suggestion,
            parent=parent
        )
        
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def suggestion_comments(request, pk):
    """Récupérer les commentaires d'une suggestion"""
    suggestion = get_object_or_404(Suggestion, pk=pk)
    
    # Récupérer seulement les commentaires principaux (pas les réponses)
    comments = Comment.objects.filter(
        suggestion=suggestion, 
        parent=None
    ).select_related('author').prefetch_related('replies__author').order_by('created_at')
    
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)

