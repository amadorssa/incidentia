from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['incident_text', 'user_creator', 'description']  
        labels = {
            'incident_text': 'Nombre',
            'user_creator': 'Agregado por',
            'description': 'Descripcion',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

