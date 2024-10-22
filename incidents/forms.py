from django import forms
from .models import Incident

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ['incident_text','prioridad', 'category', 'description', 'attachment']  
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

