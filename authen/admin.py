from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Authen

@admin.register(Authen)
class AuthenAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('telephone',)}),
    )
    list_display = ['username', 'email', 'telephone', 'is_staff']
#######
from django.contrib import admin
from .models import Bac, Matiere , Chapitre ,Cour,Commentaire

# Enregistrer les modèles dans l'admin
admin.site.register(Bac)
admin.site.register(Matiere)
admin.site.register(Chapitre)
admin.site.register(Cour)
admin.site.register(Commentaire)

