from rest_framework import serializers
from suggestionboxapp.models import  Comment
from suggestionboxapp.serializers.UserSerializer import UserSerializer



class CommentSerializer(serializers.ModelSerializer):
    """Serializer pour les commentaires"""
    author = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'parent', 'is_internal', 'replies', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.all(), many=True).data
        return []