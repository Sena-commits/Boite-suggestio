from django.db import models
from django.contrib.auth import get_user_model
import uuid
from .Suggestion import Suggestion

User = get_user_model()


class Comment(models.Model):
    """Commentaire sur une suggestion"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    is_internal = models.BooleanField(default=False)  # Commentaire entre modérateurs
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Commentaire de {self.author.username} sur {self.suggestion.title}"