from django import forms
from .models import Incident, Comentario
from django.core.exceptions import ValidationError 
from django.utils import timezone
from organizaciones.models import MiembroOrganizacion 
from cuentas.models import Usuario

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
        organizacion = kwargs.pop('organizacion', None)  # Recibe la organizacion desde la vista

        super().__init__(*args, **kwargs)

        # Guarda la organización en el formulario para usarla en otras partes
        self.organizacion = organizacion
        self.usuario = usuario

        

        if organizacion and usuario:
            self.miembro_usuario = MiembroOrganizacion.objects.filter(
                organizacion = self.organizacion,
                usuario = usuario
            ).first()
        # Checa si el usuario actual es admin para privilegios
            self.is_admin = self.miembro_usuario and self.miembro_usuario.rol == MiembroOrganizacion.ROL_ADMINISTRADOR
            if self.is_admin:
            # Filtra los usuarios que pertenecen a la organización para asignarlos en el campo 'assigned_to'
                miembros_organizacion = MiembroOrganizacion.objects.filter(organizacion=organizacion)
                self.fields['assigned_to'].queryset = miembros_organizacion # Asigna los usuarios a 'assigned_to'
            else:
                self.fields.pop('assigned_to')
        else:
            self.fields['assigned_to'].queryset = MiembroOrganizacion.objects.none()


    def clean(self): #Validaciones
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")
        assigned_to = cleaned_data.get("assigned_to")
        
        # Usa la organización guardada desde __init__
        organizacion = self.organizacion

        # Validación de fechas
        if start_date and due_date and start_date > due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")

        # Validar que el usuario asignado pertenezca a la organización
        if assigned_to and organizacion:
            if assigned_to.organizacion != organizacion:
                raise ValidationError("El usuario asignado debe pertenecer a la organización del incidente.")
                
        return cleaned_data
    
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'cols': 50, 'placeholder': 'Escribe tu comentario aquí...'}),
        }
        labels = {
            'texto': '',
        }

