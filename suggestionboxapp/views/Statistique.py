from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from suggestionboxapp.models import Category, Suggestion, Vote




@api_view(['GET'])
def public_stats(request):
    """Statistiques publiques"""
    stats = {
        'total_suggestions': Suggestion.objects.count(),
        'pending_suggestions': Suggestion.objects.filter(status='pending').count(),
        'approved_suggestions': Suggestion.objects.filter(status='approved').count(),
        'implemented_suggestions': Suggestion.objects.filter(status='implemented').count(),
        'total_votes': Vote.objects.count(),
        'active_categories': Category.objects.filter(is_active=True).count(),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_stats(request):
    """Statistiques personnelles de l'utilisateur"""
    user_suggestions = Suggestion.objects.filter(author=request.user)
    user_votes = Vote.objects.filter(user=request.user)
    
    stats = {
        'my_suggestions': user_suggestions.count(),
        'my_pending': user_suggestions.filter(status='pending').count(),
        'my_approved': user_suggestions.filter(status='approved').count(),
        'my_implemented': user_suggestions.filter(status='implemented').count(),
        'my_votes': user_votes.count(),
        'my_upvotes': user_votes.filter(vote_type='upvote').count(),
        'total_votes_received': sum(s.votes_count for s in user_suggestions),
    }
    return Response(stats)
@api_view(['GET'])
def public_stats(request):
    """Statistiques publiques"""
    stats = {
        'total_suggestions': Suggestion.objects.count(),
        'pending_suggestions': Suggestion.objects.filter(status='pending').count(),
        'approved_suggestions': Suggestion.objects.filter(status='approved').count(),
        'implemented_suggestions': Suggestion.objects.filter(status='implemented').count(),
        'total_votes': Vote.objects.count(),
        'active_categories': Category.objects.filter(is_active=True).count(),
    }
    return Response(stats)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_stats(request):
    """Statistiques personnelles de l'utilisateur"""
    user_suggestions = Suggestion.objects.filter(author=request.user)
    user_votes = Vote.objects.filter(user=request.user)
    
    stats = {
        'my_suggestions': user_suggestions.count(),
        'my_pending': user_suggestions.filter(status='pending').count(),
        'my_approved': user_suggestions.filter(status='approved').count(),
        'my_implemented': user_suggestions.filter(status='implemented').count(),
        'my_votes': user_votes.count(),
        'my_upvotes': user_votes.filter(vote_type='upvote').count(),
        'total_votes_received': sum(s.votes_count for s in user_suggestions),
    }
    return Response(stats)