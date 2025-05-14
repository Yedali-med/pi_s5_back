from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model
import logging

logger = logging.getLogger(__name__)

# Obtenir le modèle utilisateur configuré
User = get_user_model()

class SignupView(APIView):
    """
    Vue pour l'inscription des utilisateurs.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        logger.debug("SignupView called with data: %s", request.data)
        username = request.data.get('username')
        telephone = request.data.get('telephone')
        password = request.data.get('password')

        # Validation des champs requis
        if not username or not telephone or not password:
            logger.error("Missing fields: username, telephone, or password.")
            return Response({
                'success': False,
                'message': 'All fields (username, telephone, password) are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Vérifications des doublons
        if User.objects.filter(username=username).exists():
            logger.error("Username already exists.")
            return Response({
                'success': False,
                'message': 'Username already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        if hasattr(User, 'telephone') and User.objects.filter(telephone=telephone).exists():
            logger.error("Telephone number already exists.")
            return Response({
                'success': False,
                'message': 'Telephone number already exists.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Création de l'utilisateur
            user = User.objects.create_user(username=username, password=password)
            if hasattr(user, 'telephone'):
                user.telephone = telephone
            user.save()

            # Génération d'un token
            token, _ = Token.objects.get_or_create(user=user)

            logger.debug("User created successfully.")
            return Response({
                'success': True,
                'message': 'Account created successfully.',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'telephone': getattr(user, 'telephone', None),
                    'token': token.key
                }
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("An error occurred while creating the user.")
            return Response({
                'success': False,
                'message': 'An error occurred while creating the account.',
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    """
    Vue pour la connexion des utilisateurs via téléphone et mot de passe.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        logger.debug("LoginView called with data: %s", request.data)
        telephone = request.data.get('telephone')
        password = request.data.get('password')

        # Vérification des champs requis
        if not telephone or not password:
            logger.error("Missing fields: telephone or password.")
            return Response({
                'success': False,
                'message': 'Both telephone and password are required.'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Recherche de l'utilisateur avec le téléphone
        try:
            user = User.objects.get(telephone=telephone)
        except User.DoesNotExist:
            logger.error("No user found with telephone: %s", telephone)
            return Response({
                'success': False,
                'message': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)

        # Authentification de l'utilisateur
        user = authenticate(username=user.username, password=password)  # Utilisation du username
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            logger.debug("Login successful for user: %s", user.username)
            return Response({
                'success': True,
                'message': 'Login successful.',
                'data': {
                    'user_id': user.id,
                    'username': user.username,
                    'telephone': user.telephone,
                    'token': token.key
                }
            }, status=status.HTTP_200_OK)
        else:
            logger.error("Invalid password for user with telephone: %s", telephone)
            return Response({
                'success': False,
                'message': 'Invalid credentials.'
            }, status=status.HTTP_401_UNAUTHORIZED)

#############
from rest_framework import viewsets
from .models import Bac
from .serializers import BacSerializer

class BacViewSet(viewsets.ModelViewSet):
    queryset = Bac.objects.all()
    serializer_class = BacSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Matiere
from .serializers import MatiereSerializer

class MatieresParBacAPIView(APIView):
    def get(self, request, bac_id):
        try:
            # Récupérer les matières associées à l'ID du Bac
            matieres = Matiere.objects.filter(bac_id=bac_id)
            serializer = MatiereSerializer(matieres, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Matiere.DoesNotExist:
            return Response({"error": "Aucune matière trouvée pour ce Bac"}, status=status.HTTP_404_NOT_FOUND)
###########
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Chapitre
from .serializers import ChapitreSerializer

class ChapitreAPIView(APIView):
    def get(self, request, matiere_id=None):
        if matiere_id:
            chapitres = Chapitre.objects.filter(matiere_id=matiere_id)  # Filtrer les chapitres par matière
        else:
            chapitres = Chapitre.objects.all()  # Tous les chapitres
        serializer = ChapitreSerializer(chapitres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
#########
from rest_framework import viewsets
from .models import Cour
from .serializers import CourSerializer

class CourViewSet(viewsets.ModelViewSet):
    queryset = Cour.objects.all()  # Tous les cours
    serializer_class = CourSerializer


############
from django.shortcuts import render

def accueil(request):
    return render(request, 'accueil.html')  
########
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Bac 
from .forms import BacForm

# BAC CRUD
class BacListView(ListView):
    model = Bac
    template_name = 'bac/list.html'
    context_object_name = 'bacs'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['form'] = BacForm() 
    #     # print("✅ Formulaire chargé :", context['form']) # ✅ Passer le formulaire dans le contexte
    #     return context

class BacDetailView(DetailView):
    model = Bac
    template_name = 'bac/detail.html'
    context_object_name = 'bac'

    

class BacCreateView(CreateView):
    model = Bac
    form_class = BacForm
    template_name = 'bac/form.html'
    success_url = reverse_lazy('bac_list')

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image')  # ✅ Gérer l'upload de l'image
        return super().form_valid(form)

class BacUpdateView(UpdateView):
    model = Bac
    form_class = BacForm
    template_name = 'bac/form.html'
    success_url = reverse_lazy('bac_list')

    def form_valid(self, form):
        form.instance.image = self.request.FILES.get('image', form.instance.image)  # ✅ Gérer la mise à jour de l'image
        return super().form_valid(form)

class BacDeleteView(DeleteView):
    model = Bac
    template_name = 'bac/delete.html'
    success_url = reverse_lazy('bac_list')
######## matiere
from django.shortcuts import render, get_object_or_404, redirect
from .models import Matiere
from .forms import MatiereForm

# 🔹 Afficher la liste des matières
def matiere_list(request):
    matieres = Matiere.objects.all()
    bacs = Bac.objects.all()
    return render(request, 'Matiere/matiere_list.html', {'matieres': matieres, 'bacs': bacs})

def matiere_create(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        bac_id = request.POST.get("bac_id")
        image = request.FILES.get("image")
        if nom and bac_id:
            Matiere.objects.create(nom=nom, bac_id=bac_id, image=image)
    return redirect('matiere_list')

def matiere_update(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == "POST":
        matiere.nom = request.POST.get("nom")
        matiere.bac_id = request.POST.get("bac_id")
        if request.FILES.get("image"):
            matiere.image = request.FILES.get("image")
        matiere.save()
    return redirect('matiere_list')

def matiere_delete(request, pk):
    matiere = get_object_or_404(Matiere, pk=pk)
    if request.method == "POST":
        matiere.delete()
    return redirect('matiere_list')

from django.shortcuts import render, get_object_or_404, redirect
from .models import Chapitre, Matiere
from .forms import ChapitreForm
# ✅ Afficher la liste des chapitres
def chapitre_list(request):
    chapitres = Chapitre.objects.all()
    form_create = ChapitreForm()  # Formulaire pour ajouter un chapitre
    
    # Créer un formulaire de modification pour chaque chapitre
    form_update = {chapitre.id: ChapitreForm(instance=chapitre) for chapitre in chapitres}
    
    return render(request, 'chapitres/chapitre_list.html', {
        'chapitres': chapitres,
        'form_create': form_create,
        'form_update': form_update,  # Passer les formulaires de modification
    })

# Créer un chapitre (modifié pour l'utiliser avec le modal)
def chapitre_create(request):
    if request.method == 'POST':
        form = ChapitreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('chapitre_list')
        else:
            print(form.errors)  # Afficher les erreurs du formulaire pour déboguer
    return redirect('chapitre_list')

# Modifier un chapitre (modifié pour l'utiliser avec le modal)
def chapitre_update(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)

    if request.method == 'POST':
        form = ChapitreForm(request.POST, instance=chapitre)
        if form.is_valid():
            form.save()
    
    # Toujours rediriger après POST (PRG pattern)
    return redirect('chapitre_list')
# Détail d'un chapitre
def chapitre_detail(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    return render(request, 'chapitres/chapitre_list.html', {'chapitre': chapitre})

# Supprimer un chapitre (modifié pour l'utiliser avec le modal)
def chapitre_delete(request, chapitre_id):
    chapitre = get_object_or_404(Chapitre, id=chapitre_id)
    if request.method == 'POST':
        chapitre.delete()
        return redirect('chapitre_list')  # Redirection vers la liste après suppression
    return redirect('chapitre_list')
# ✅ Page de confirmation
######## cour
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cour
from .forms import CourForm


class CourListView(ListView):
    model = Cour
    template_name = 'cour/cour_list.html'
    context_object_name = 'cours'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_create'] = CourForm()
        context['chapitres'] = Chapitre.objects.all()
        return context


class CourCreateView(CreateView):
    model = Cour
    fields = ['titre', 'video', 'chapitre']
    success_url = reverse_lazy('cour_list')
    template_name = 'cour/cour_list.html'  # fallback en cas d'erreur

    def form_invalid(self, form):
        # Si le formulaire est invalide, renvoyer tous les cours et le formulaire avec erreurs
        cours = Cour.objects.all()
        chapitres = Chapitre.objects.all()
        return self.render_to_response(self.get_context_data(
            form_create=form, cours=cours, chapitres=chapitres
        ))

class CourUpdateView(UpdateView):
    model = Cour
    fields = ['titre', 'video', 'chapitre']
    success_url = reverse_lazy('cour_list')
    template_name = 'cour/cour_list.html'

    def form_invalid(self, form):
        cours = Cour.objects.all()
        chapitres = Chapitre.objects.all()
        return self.render_to_response(self.get_context_data(
            form=form, cours=cours, chapitres=chapitres
        ))

class CourDeleteView(DeleteView):
    model = Cour
    template_name = 'cour/cour_list.html'
    success_url = reverse_lazy('cour_list')
############
# views.py
from rest_framework import generics
from .models import Cour
from .serializers import CourSerializer

class CoursListAPIView(generics.ListAPIView):
    serializer_class = CourSerializer

    def get_queryset(self):
        chapitre_id = self.kwargs.get('chapitre_id')
        return Cour.objects.filter(chapitre_id=chapitre_id)
def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, 'video_detail.html', {'video': video})
##############

##########
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Commentaire, CommentaireReaction
from .serializers import CommentaireSerializer, CommentaireReactionSerializer

class CommentaireViewSet(viewsets.ModelViewSet):
    """
    API permettant de gérer les commentaires des cours et les réactions (like/dislike).
    """
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Lors de la création d’un commentaire, l’utilisateur connecté est automatiquement assigné.
        """
        serializer.save(utilisateur=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Ajouter un like au commentaire.
        """
        commentaire = get_object_or_404(Commentaire, pk=pk)
        if commentaire.ajouter_reaction(request.user, 'like'):
            return Response({
                'message': 'Like ajouté',
                'likes': commentaire.likes,
                'dislikes': commentaire.dislikes
            })
        return Response({'message': 'Vous avez déjà liké ce commentaire.'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def dislike(self, request, pk=None):
        """
        Ajouter un dislike au commentaire.
        """
        commentaire = get_object_or_404(Commentaire, pk=pk)
        if commentaire.ajouter_reaction(request.user, 'dislike'):
            return Response({
                'message': 'Dislike ajouté',
                'likes': commentaire.likes,
                'dislikes': commentaire.dislikes
            })
        return Response({'message': 'Vous avez déjà mis un dislike sur ce commentaire.'}, status=400)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def remove_reaction(self, request, pk=None):
        """
        Supprimer la réaction (like/dislike) de l'utilisateur sur ce commentaire.
        """
        commentaire = get_object_or_404(Commentaire, pk=pk)
        if commentaire.supprimer_reaction(request.user):
            return Response({
                'message': 'Réaction supprimée',
                'likes': commentaire.likes,
                'dislikes': commentaire.dislikes
            })
        return Response({'message': 'Aucune réaction trouvée pour cet utilisateur.'}, status=400)
#############
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from authen.models import Authen  # Assure-toi que ce modèle est correct
from rest_framework import serializers

# Serializer pour renvoyer les données nécessaires
class AuthenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Authen
        fields = ['id', 'username', 'telephone']

@api_view(['GET'])
def get_user_info(request, user_id):
    try:
        user = Authen.objects.get(id=user_id)
        serializer = AuthenSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Authen.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=status.HTTP_404_NOT_FOUND)
###########
def login(request):
    if request.method == 'POST':
        login_value = request.POST.get('login')
        mot_de_passe = request.POST.get('pwd')

        try:
            inscription = Inscription.objects.get(login=login_value)
            if check_password(mot_de_passe, inscription.mot_de_passe):
                return redirect('home')
            else:
                error_message = "Login or password is incorrect."
                return render(request, 'login.html', {'error_message': error_message})

        except Inscription.DoesNotExist:
            error_message = "Login or password is incorrect."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')
######
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import Inscription
from django.contrib.auth.hashers import check_password


def inscription(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        mot_de_passe = request.POST.get('pwd')
        confPwd = request.POST.get('confPwd')

        if mot_de_passe == confPwd:
            hashed_password = make_password(mot_de_passe)
            inscription = Inscription(login=login, mot_de_passe=hashed_password)
            inscription.save()
            return redirect('login')  # Redirige vers la page de connexion après l'inscription
        else:
            error_message = "Les mots de passe ne correspondent pas."
            return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')
from django.shortcuts import render

def home(request):
    bacs = Bac.objects.all()  # Récupérer tous les objets Bac
    return render(request, 'bac/list.html', {'bacs': bacs})
####
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    """
    Déconnecte l'utilisateur et le redirige vers la page de login.
    """
    logout(request)
    return redirect('login')  # Assurez-vous que 'login' est le nom de l'URL de connexion
