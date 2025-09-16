from rest_framework import serializers
from suggestionboxapp.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer pour les catégories"""
    suggestions_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'icon', 'is_active', 'suggestions_count']
    
    def get_suggestions_count(self, obj):
        return obj.suggestion_set.filter(status__in=['pending', 'in_review', 'approved']).count()
