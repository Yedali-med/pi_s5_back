# signals.py (vide ou contenant uniquement des signaux pour Authen)

# Exemple de signal si vous voulez ajouter de la logique spécifique à Authen
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Authen

@receiver(post_save, sender=Authen)
def on_authen_save(sender, instance, created, **kwargs):
    if created:
        print(f"Utilisateur créé : {instance.username}")
