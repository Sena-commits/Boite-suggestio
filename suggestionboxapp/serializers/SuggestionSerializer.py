from rest_framework import serializers
from suggestionboxapp.models import  Suggestion
from suggestionboxapp.serializers import (UserSerializer, VoteSerializer, CategorySerializer, CommentSerializer)

from suggestionboxapp.serializers.UserSerializer import UserSerializer
from rest_framework import serializers
from .UserSerializer import UserSerializer
from .CategorySerializer import CategorySerializer
from .CommentSerializer import CommentSerializer
from .VoteSerializer import VoteSerializer
from suggestionboxapp.models import Suggestion


class SuggestionListSerializer(serializers.ModelSerializer):
    """Serializer pour la liste des suggestions (version allégée)"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Suggestion
        fields = [
            'id', 'title', 'description', 'category', 'status', 'priority',
            'author', 'is_anonymous', 'votes_count', 'views_count', 'user_vote',
            'created_at', 'updated_at'
        ]
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.votes.filter(user=request.user).first()
            return VoteSerializer(vote).data if vote else None
        return None

class SuggestionDetailSerializer(serializers.ModelSerializer):
    """Serializer détaillé pour une suggestion"""
    author = UserSerializer(read_only=True)
    assigned_to = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.UUIDField(write_only=True, required=False)
    comments = CommentSerializer(many=True, read_only=True)
    user_vote = serializers.SerializerMethodField()
    can_edit = serializers.SerializerMethodField()
    
    class Meta:
        model = Suggestion
        fields = [
            'id', 'title', 'description', 'category', 'category_id', 'status', 'priority',
            'author', 'assigned_to', 'is_anonymous', 'tracking_code', 'views_count', 
            'votes_count', 'comments', 'user_vote', 'can_edit',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'tracking_code', 'views_count', 'votes_count']
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.votes.filter(user=request.user).first()
            return VoteSerializer(vote).data if vote else None
        return None
    
    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request:
            return False
        
        user = request.user
        
        # Super utilisateurs peuvent tout modifier
        if user.is_authenticated and user.is_moderator_or_admin:
            return True
        
        # Auteur peut modifier sa propre suggestion
        if user.is_authenticated and obj.author == user:
            return True
        
        return False

class AnonymousSuggestionSerializer(serializers.ModelSerializer):
    """Serializer spécialement pour les suggestions anonymes"""
    anonymous_email = serializers.EmailField(required=False, allow_blank=True)
    category_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Suggestion
        fields = [
            'id', 'title', 'description', 'category_id', 'anonymous_email',
            'tracking_code', 'created_at'
        ]
        read_only_fields = ['id', 'tracking_code']
    
    def create(self, validated_data):
        validated_data['is_anonymous'] = True
        return super().create(validated_data)