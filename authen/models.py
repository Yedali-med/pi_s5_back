from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class Authen(AbstractUser):
    telephone = models.CharField(max_length=15, unique=True, null=True, blank=False)

    # Champs pour éviter les conflits
    groups = models.ManyToManyField(
        Group,
        related_name="authen_user_set",  # Nom explicite pour éviter le conflit
        blank=True,
        help_text="Les groupes auxquels cet utilisateur appartient.",
        verbose_name="groupes",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="authen_user_set",  # Nom explicite pour éviter le conflit
        blank=True,
        help_text="Les autorisations spécifiques pour cet utilisateur.",
        verbose_name="permissions utilisateur",
    )

    def __str__(self):
        return self.username


  ##################

class Bac(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='bac_images/', blank=True, null=True)
    def __str__(self):
        return self.nom  # Retourne le nom du bac pour une meilleure lisibilité

class Matiere(models.Model):
    nom = models.CharField(max_length=255)
    bac = models.ForeignKey('Bac', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='matiere_images/', blank=True, null=True)  # Assurez-vous que l'upload est correct

    def __str__(self):
        return self.nom # Retourne le nom de la matière avec son bac associé
###########
class Chapitre(models.Model):
    id = models.AutoField(primary_key=True)  # ID unique pour chaque chapitre
    titre = models.CharField(max_length=255)  # Titre du chapitre (ex: "Génétique")
    numero = models.PositiveIntegerField()  # Numéro du chapitre (ex: 1, 2, 3)
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.CASCADE,
        related_name='chapitres'  # Permet d'accéder aux chapitres via Matière (ex: matiere.chapitres.all())
    )
    nombre_de_lecons = models.PositiveIntegerField(default=0)  # Nombre de leçons associées

    def __str__(self):
        return f"{self.numero}. {self.titre} ({self.matiere.nom})"

  #############


class Cour(models.Model):
    id = models.AutoField(primary_key=True)  # ID unique pour chaque cours
    titre = models.CharField(max_length=255)  # Titre du cours
    video = models.FileField(upload_to='videos/', blank=True, null=True)  # Fichier vidéo associé au cours
    chapitre = models.ForeignKey(
        'Chapitre',
        on_delete=models.CASCADE,  # Supprime les cours si le chapitre est supprimé
        related_name='cours'  # Permet d'accéder aux cours via chapitre.cours.all()
    )

    def __str__(self):
        return self.titre
###############

######################
from django.db import models
from django.conf import settings  # Utilisation du modèle utilisateur personnalisé

class Commentaire(models.Model):
    cours = models.ForeignKey(
        'Cour', 
        on_delete=models.CASCADE, 
        related_name='commentaires'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Remplace User par Authen
        on_delete=models.CASCADE, 
        related_name='commentaires'
    )
    parent = models.ForeignKey(
        'self',  
        on_delete=models.CASCADE, 
        related_name='reponses',
        blank=True, 
        null=True
    )
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-date_creation']

    def __str__(self):
        return f"Commentaire de {self.utilisateur.username} sur {self.cours.titre}"

    def mettre_a_jour_reactions(self):
        """Met à jour les compteurs de likes et dislikes"""
        self.likes = self.reactions.filter(reaction_type='like').count()
        self.dislikes = self.reactions.filter(reaction_type='dislike').count()
        self.save()

    def ajouter_reaction(self, utilisateur, reaction_type):
        """Ajoute ou modifie une réaction (like/dislike)"""
        reaction, created = CommentaireReaction.objects.get_or_create(
            commentaire=self, utilisateur=utilisateur
        )
        if not created and reaction.reaction_type == reaction_type:
            return False  # L'utilisateur a déjà mis cette réaction
        reaction.reaction_type = reaction_type
        reaction.save()
        self.mettre_a_jour_reactions()
        return True

    def supprimer_reaction(self, utilisateur):
        """Supprime la réaction de l'utilisateur"""
        reaction = CommentaireReaction.objects.filter(commentaire=self, utilisateur=utilisateur).first()
        if reaction:
            reaction.delete()
            self.mettre_a_jour_reactions()
            return True
        return False


class CommentaireReaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike')
    ]

    commentaire = models.ForeignKey(
        Commentaire, 
        on_delete=models.CASCADE, 
        related_name='reactions'
    )
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Remplace User par Authen
        on_delete=models.CASCADE
    )
    reaction_type = models.CharField(
        max_length=10, 
        choices=REACTION_CHOICES
    )

    class Meta:
        unique_together = ('commentaire', 'utilisateur')  # Empêcher un utilisateur d'avoir plusieurs réactions
#########
class Inscription(models.Model):
    login = models.CharField(max_length=100)
    mot_de_passe = models.CharField(max_length=128)
    confPwd = models.CharField(max_length=128)