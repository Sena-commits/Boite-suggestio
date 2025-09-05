from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
import uuid
import string
import random
from .Category import Category

User = get_user_model()

class Suggestion(models.Model):
    """Modèle principal des suggestions"""
    
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        IN_REVIEW = 'in_review', 'En cours d\'examen'
        APPROVED = 'approved', 'Approuvée'
        REJECTED = 'rejected', 'Rejetée'
        IMPLEMENTED = 'implemented', 'Mise en œuvre'
        ARCHIVED = 'archived', 'Archivée'
    
    class Priority(models.TextChoices):
        LOW = 'low', 'Faible'
        MEDIUM = 'medium', 'Moyenne'
        HIGH = 'high', 'Élevée'
        URGENT = 'urgent', 'Urgente'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    
    # Author (peut être null pour suggestions anonymes)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='suggestions')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_suggestions')
    
    # Champs pour suggestions anonymes
    is_anonymous = models.BooleanField(default=False)
    tracking_code = models.CharField(max_length=20, unique=True, blank=True)
    anonymous_email = models.EmailField(blank=True)
    can_edit_until = models.DateTimeField(null=True, blank=True)
    
    # Métriques
    views_count = models.PositiveIntegerField(default=0)
    votes_count = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.is_anonymous and not self.tracking_code:
            self.tracking_code = self.generate_tracking_code()
            # 48h pour modifier une suggestion anonyme
            self.can_edit_until = timezone.now() + timezone.timedelta(hours=48)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_tracking_code():
        """Génère un code de suivi unique"""
        year = timezone.now().year
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"SG-{year}-{random_part}"

    @property
    def can_be_edited_anonymously(self):
        """Vérifie si une suggestion anonyme peut encore être modifiée"""
        if not self.is_anonymous or not self.can_edit_until:
            return False
        return timezone.now() <= self.can_edit_until
