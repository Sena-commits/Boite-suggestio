from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    ROLES = (
        ('EMPLOYE', 'Employé'),
        ('ADMIN', 'Administrateur'),
    )
    role = models.CharField(max_length=20, choices=ROLES, default='EMPLOYE')

class Suggestion(models.Model):
    STATUTS = (
        ('EN_ATTENTE', 'En attente'),
        ('VALIDEE', 'Validée'),
        ('REJETEE', 'Rejetée'),
    )
    titre = models.CharField(max_length=255)
    description = models.TextField()
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='EN_ATTENTE')
    est_anonyme = models.BooleanField(default=False)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.SET_NULL, null=True, blank=True)

class Commentaire(models.Model):
    contenu = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    suggestion = models.ForeignKey(Suggestion, on_delete=models.CASCADE, related_name='commentaires')

