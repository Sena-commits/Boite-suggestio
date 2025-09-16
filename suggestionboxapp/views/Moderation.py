from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from suggestionboxapp.models import  Suggestion
from suggestionboxapp.permissions import IsModeratorOrAdmin

User = get_user_model()


@api_view(['PATCH'])
@permission_classes([IsModeratorOrAdmin])
def change_suggestion_status(request, pk):
    """Changer le statut d'une suggestion (modérateurs/admins seulement)"""
    suggestion = get_object_or_404(Suggestion, pk=pk)
    new_status = request.data.get('status')
    
    if new_status not in dict(Suggestion.Status.choices):
        return Response({
            'error': 'Statut invalide'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    old_status = suggestion.status
    suggestion.status = new_status
    suggestion.save(update_fields=['status'])
    
    return Response({
        'message': f'Statut changé de {old_status} à {new_status}',
        'old_status': old_status,
        'new_status': new_status
    })

@api_view(['PATCH'])
@permission_classes([IsModeratorOrAdmin])
def assign_suggestion(request, pk):
    """Assigner une suggestion à un utilisateur"""
    suggestion = get_object_or_404(Suggestion, pk=pk)
    assigned_to_id = request.data.get('assigned_to_id')
    
    if assigned_to_id:
        assigned_user = get_object_or_404(User, pk=assigned_to_id)
        suggestion.assigned_to = assigned_user
        message = f'Suggestion assignée à {assigned_user.username}'
    else:
        suggestion.assigned_to = None
        message = 'Assignation supprimée'
    
    suggestion.save(update_fields=['assigned_to'])
    
    return Response({
        'message': message,
        'assigned_to': suggestion.assigned_to.username if suggestion.assigned_to else None
    })