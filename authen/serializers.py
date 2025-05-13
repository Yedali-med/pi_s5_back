from rest_framework import serializers
from .models import Authen

class AuthenSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Authen
        fields = ['username', 'telephone', 'password']

    def create(self, validated_data):
        user = Authen.objects.create_user(
            username=validated_data['username'],
            telephone=validated_data['telephone'],
            password=validated_data['password']
        )
        return user

class AuthenLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

############
from rest_framework import serializers
from .models import Bac

class BacSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bac
        fields = '__all__'  # Champs que vous voulez inclure dans l'API
########
from rest_framework import serializers
from .models import Matiere

class MatiereSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True, use_url=True)  # Retourne l'URL complète

    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'bac', 'image']# Champs à inclure dans l'API

##########
from rest_framework import serializers
from .models import Chapitre

class ChapitreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapitre
        fields = ['id', 'titre', 'numero', 'nombre_de_lecons', 'matiere_id']  # Inclure tous les champs nécessaires
#######
from rest_framework import serializers
from .models import Cour

class CourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cour
        fields = ['id', 'titre', 'video', 'chapitre'] # Champs à inclure dans l'API


###################
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'telephone', 'profile_image']
################
from rest_framework import serializers
from .models import Commentaire, CommentaireReaction

class CommentaireSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.ReadOnlyField(source='utilisateur.username')
    reponses = serializers.SerializerMethodField()

    class Meta:
        model = Commentaire
        fields = [
            'id', 'cours', 'utilisateur', 'utilisateur_nom',
            'parent', 'contenu', 'date_creation', 'likes', 'dislikes', 'reponses'
        ]
        read_only_fields = ['utilisateur', 'likes', 'dislikes', 'date_creation']

    def get_reponses(self, obj):
        reponses = obj.reponses.all().order_by('date_creation')
        return CommentaireSerializer(reponses, many=True, context=self.context).data


class CommentaireReactionSerializer(serializers.ModelSerializer):
    utilisateur_nom = serializers.ReadOnlyField(source='utilisateur.username')

    class Meta:
        model = CommentaireReaction
        fields = ['id', 'commentaire', 'utilisateur', 'utilisateur_nom', 'reaction_type']
        read_only_fields = ['utilisateur', 'utilisateur_nom']
