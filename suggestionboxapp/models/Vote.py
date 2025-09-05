from django.db import models
from django.contrib.auth import get_user_model
import uuid
from .Suggestion import Suggestion


User = get_user_model()


class Vote(models.Model):
    """Vote sur une suggestion"""
    
    class VoteType(models.TextChoices):
        UPVOTE = 'upvote', 'Vote positif'
        DOWNVOTE = 'downvote', 'Vote négatif'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='votes')
    vote_type = models.CharField(max_length=10, choices=VoteType.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'suggestion')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Mise à jour du compteur de votes
        self.update_suggestion_votes_count()
    
    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.update_suggestion_votes_count()
    
    def update_suggestion_votes_count(self):
        """Met à jour le compteur de votes de la suggestion"""
        upvotes = self.suggestion.votes.filter(vote_type='upvote').count()
        downvotes = self.suggestion.votes.filter(vote_type='downvote').count()
        self.suggestion.votes_count = upvotes - downvotes
        self.suggestion.save(update_fields=['votes_count'])
