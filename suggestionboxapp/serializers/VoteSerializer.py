from rest_framework import serializers
from suggestionboxapp.models import  Vote


class VoteSerializer(serializers.ModelSerializer):
    """Serializer pour les votes"""
    class Meta:
        model = Vote
        fields = ['id', 'vote_type', 'created_at']
        read_only_fields = ['id']