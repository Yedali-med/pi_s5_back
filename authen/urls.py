from django.urls import path
from .views import SignupView, LoginView

########
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BacViewSet, MatieresParBacAPIView, ChapitreAPIView, CourViewSet
from .views import BacListView, BacDetailView, BacCreateView, BacUpdateView, BacDeleteView
from .views import matiere_list, matiere_create, matiere_update, matiere_delete
from .views import chapitre_list, chapitre_detail, chapitre_create, chapitre_update, chapitre_delete
from .views import CourListView, CourCreateView, CourUpdateView, CourDeleteView
from .views import CoursListAPIView
from .views import get_user_info
from . import views

# Créer les routers pour les ViewSets
router = DefaultRouter()
router.register(r'bacs', BacViewSet, basename='bac')  # URL pour le modèle Bac
router.register(r'cours', CourViewSet, basename='cours')  # URL pour le modèle Cour
from django.urls import path
from .views import profile_view
# Combiner toutes les URLs
from .views import CommentaireViewSet

commentaire_list = CommentaireViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

commentaire_detail = CommentaireViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

commentaire_like = CommentaireViewSet.as_view({
    'post': 'like'
})

commentaire_dislike = CommentaireViewSet.as_view({
    'post': 'dislike'
})

commentaire_remove_reaction = CommentaireViewSet.as_view({
    'post': 'remove_reaction'
})
##############
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    # Inclure les routes des ViewSets
    path('api/', include(router.urls)),

    # Route pour les matières par Bac
    path('api/matieres/<int:bac_id>/', MatieresParBacAPIView.as_view(), name='matieres_par_bac'),

    # Routes pour les chapitres
    path('api/chapitres/', ChapitreAPIView.as_view(), name='chapitres_all'),
    path('api/chapitres/<int:matiere_id>/', ChapitreAPIView.as_view(), name='chapitres_by_matiere'),

    ######
    # BAC
    path('bacs/', BacListView.as_view(), name='bac_list'),
    path('bacs/<int:pk>/', BacDetailView.as_view(), name='bac_detail'),
    path('bacs/new/', BacCreateView.as_view(), name='bac_create'),
    path('bacs/<int:pk>/edit/', BacUpdateView.as_view(), name='bac_update'),
    path('bacs/<int:pk>/delete/', BacDeleteView.as_view(), name='bac_delete'),
    ######
    path('matieres/', matiere_list, name='matiere_list'),
    path('matieres/ajouter/', matiere_create, name='matiere_create'),
    path('matieres/modifier/<int:pk>/', matiere_update, name='matiere_update'),
    path('matieres/supprimer/<int:pk>/', matiere_delete, name='matiere_delete'),
    ########
    path('chapitres/', chapitre_list, name='chapitre_list'),
    path('chapitres/<int:chapitre_id>/', chapitre_detail, name='chapitre_detail'),
    path('chapitres/new/', chapitre_create, name='chapitre_create'),
    path('chapitres/<int:chapitre_id>/edit/', chapitre_update, name='chapitre_update'),
    path('chapitres/<int:chapitre_id>/delete/', chapitre_delete, name='chapitre_delete'),
    ########## cour
    path('cours/', CourListView.as_view(), name='cour_list'),
    path('cours/ajouter/', CourCreateView.as_view(), name='cour_create'),
    path('cours/<int:pk>/modifier/', CourUpdateView.as_view(), name='cour_update'),
    path('cours/<int:pk>/supprimer/', CourDeleteView.as_view(), name='cour_delete'),
    path('api/cours-chapitre/<int:chapitre_id>/', CoursListAPIView.as_view(), name='cours-list'),
    ###########
    path('profile/', profile_view, name='profile'),  # ✅ Route API Profile
    ############
    path('commentaires/', commentaire_list, name='commentaire-liste'),
    path('commentaires/<int:pk>/', commentaire_detail, name='commentaire-detail'),
    path('commentaires/<int:pk>/like/', commentaire_like, name='commentaire-like'),
    path('commentaires/<int:pk>/dislike/', commentaire_dislike, name='commentaire-dislike'),
    path('commentaires/<int:pk>/remove_reaction/', commentaire_remove_reaction, name='commentaire-remove-reaction'),
    path('user_info/<int:user_id>/', get_user_info),

]
