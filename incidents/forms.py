from django import forms
from .models import Incident
from django.core.exceptions import ValidationError 
from django.utils import timezone
from organizaciones.models import MiembroOrganizacion 

class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        # Creador de incidente se autoasigna y no se debe cambiar
        fields = ['incident_text', 'assigned_to', 'description','prioridad', 'category', 'attachment', 'start_date', 'due_date', 'estado']    
        labels = {
            'incident_text': 'Nombre',
            #'user_creator': 'Creador',
            'assigned_to': 'Asignar a',
            'description': 'Descripción',
            'start_date': 'Fecha de inicio',
            'due_date': 'Fecha de vencimiento',
            'attachment': 'Adjunto',
            'prioridad': 'Prioridad',
            'category': 'Categoría',
            'estado': 'Estado',
            'related_incidents': 'Incidentes relacionados',
        }

        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'related_incidents': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        # Obtén la organización de la solicitud del usuario
        usuario = kwargs.pop('usuario', None)  # Recibe el usuario desde la vista
        organizacion = usuario.miembros.first().organizacion if usuario else None

        super().__init__(*args, **kwargs)

        if organizacion:
            # Filtra los usuarios que pertenecen a la organización para asignarlos en el campo 'assigned_to'
            usuarios_organizacion = MiembroOrganizacion.objects.filter(organizacion=organizacion).values_list('usuario', flat=True)
            self.fields['assigned_to'].queryset = usuarios_organizacion  # Asigna los usuarios a 'assigned_to'
        else:
            self.fields['assigned_to'].queryset = []

    def clean(self):  # Validaciones
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")
        assigned_to = cleaned_data.get("assigned_to")
        pub_date = self.instance.pub_date if self.instance.pk else timezone.now()

        # Validación de fechas
        if start_date and due_date and start_date > due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")

        # Verificar que el usuario asignado pertenezca a la organización
        if assigned_to and self.instance.organizacion and assigned_to not in self.instance.organizacion.miembros.values_list('usuario', flat=True):
            raise ValidationError("El usuario asignado debe pertenecer a la organización del incidente.")

        return cleaned_data



