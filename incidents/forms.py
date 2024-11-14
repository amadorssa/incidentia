from django import forms
from .models import Incident
from django.core.exceptions import ValidationError 
from django.utils import timezone 

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        # Creador de incidente se autoasigna y no se debe cambiar
        #fields = ['incident_text', 'user_creator', 'description','prioridad', 'category', 'attachment', 'start_date', 'due_date']
        fields = ['incident_text', 'description','prioridad', 'category', 'attachment', 'start_date', 'due_date']  
        labels = {
            'incident_text': 'Nombre',
            #'user_creator': 'Creador',
            # 'assign': 'Asignar a',
            'description': 'Descripción',
            'start_date': 'Fecha de inicio',
            'due_date': 'Fecha de vencimiento',
            'attachment': 'Adjunto',
            'prioridad': 'Prioridad',
            'category': 'Categoría',
            'related_incidents': 'Incidentes relacionados',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'related_incidents': forms.SelectMultiple(attrs={'class': 'form-control'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")
        pub_date = self.instance.pub_date if self.instance.pk else timezone.now()

        if start_date and due_date and start_date > due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")

        return cleaned_data



