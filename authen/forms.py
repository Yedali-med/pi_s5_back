from django import forms
from .models import Bac, Matiere

class BacForm(forms.ModelForm):
    class Meta:
        model = Bac
        fields = ['nom', 'description', 'image']


###### matiere
from django import forms
from .models import Matiere

class MatiereForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Matiere
        fields = ['nom', 'bac', 'image']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'bac': forms.Select(attrs={'class': 'form-control'}),
        }
######
from django import forms
from .models import Chapitre

class ChapitreForm(forms.ModelForm):
    class Meta:
        model = Chapitre
        fields = ['titre', 'numero', 'matiere', 'nombre_de_lecons']
from django import forms
from .models import Cour

class CourForm(forms.ModelForm):
    class Meta:
        model = Cour
        fields = ['titre', 'video', 'chapitre']
