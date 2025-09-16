from rest_framework import  status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404

from suggestionboxapp.models import  Suggestion
from suggestionboxapp.serializers.SuggestionSerializer import SuggestionDetailSerializer, AnonymousSuggestionSerializer




@api_view(['POST'])
@permission_classes([AllowAny])
def create_anonymous_suggestion(request):
    """Créer une suggestion anonyme"""
    serializer = AnonymousSuggestionSerializer(data=request.data)
    if serializer.is_valid():
        suggestion = serializer.save()
        return Response({
            'tracking_code': suggestion.tracking_code,
            'message': 'Suggestion créée avec succès',
            'can_edit_until': suggestion.can_edit_until,
            'id': suggestion.id
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([AllowAny])
def track_suggestion(request, tracking_code):
    """Suivre ou modifier une suggestion via son code de suivi"""
    suggestion = get_object_or_404(Suggestion, tracking_code=tracking_code, is_anonymous=True)
    
    if request.method == 'GET':
        serializer = SuggestionDetailSerializer(suggestion, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        if not suggestion.can_be_edited_anonymously:
            return Response({
                'error': 'La période de modification est expirée'
            }, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AnonymousSuggestionSerializer(suggestion, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

