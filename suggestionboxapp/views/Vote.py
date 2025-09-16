from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from suggestionboxapp.models import  Suggestion, Vote




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_suggestion(request, pk):
    """Voter pour une suggestion"""
    suggestion = get_object_or_404(Suggestion, pk=pk)
    vote_type = request.data.get('vote_type')
    
    if vote_type not in ['upvote', 'downvote']:
        return Response({
            'error': 'vote_type doit être "upvote" ou "downvote"'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Vérifier si l'utilisateur a déjà voté
    try:
        existing_vote = Vote.objects.get(user=request.user, suggestion=suggestion)
        
        if existing_vote.vote_type == vote_type:
            # Annuler le vote
            existing_vote.delete()
            return Response({
                'message': 'Vote annulé',
                'action': 'removed'
            })
        else:
            # Changer le vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
            return Response({
                'message': f'Vote changé pour {vote_type}',
                'action': 'changed',
                'vote_type': vote_type
            })
            
    except Vote.DoesNotExist:
        # Créer un nouveau vote
        Vote.objects.create(
            user=request.user,
            suggestion=suggestion,
            vote_type=vote_type
        )
        return Response({
            'message': f'Vote {vote_type} enregistré',
            'action': 'created',
            'vote_type': vote_type
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_votes(request):
    """Récupérer les votes de l'utilisateur connecté"""
    votes = Vote.objects.filter(user=request.user).select_related('suggestion')
    data = []
    
    for vote in votes:
        data.append({
            'suggestion_id': vote.suggestion.id,
            'suggestion_title': vote.suggestion.title,
            'vote_type': vote.vote_type,
            'created_at': vote.created_at
        })
    
    return Response(data)
