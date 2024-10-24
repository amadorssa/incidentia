import datetime
from django.db import models
from django.utils import timezone
#from markdownx.models import MarkdownxField

class Incident(models.Model):
    PRIORIDAD_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    CATEGORY_CHOICES = [
        ('RENDIMIENTO', 'Rendimiento'),
        ('UI', 'UI'),
        ('DOCUMENTACION', 'Documentación'),
        ('APIS', 'API’s'),
        ('BASEDATOS', 'Bases de datos'),
        ('SEGURIDAD', 'Seguridad'),
        ('DEPENDENCIAS', 'Dependencias de terceros'),
    ]

    incident_text = models.CharField(max_length=200, null=True, blank=True)
    user_creator = models.CharField(max_length=16) #Cambiar por usuario con sesion iniciada
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(null=True, blank=True)  # Campo de descripción con soporte Markdown
    prioridad = models.CharField(max_length=7, choices=PRIORIDAD_CHOICES, default='MEDIA')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    attachment = models.FileField(upload_to='media/', null=True, blank=True)  # Subir archivos opcional

    
    start_date = models.DateTimeField('Fecha de inicio', null=True, blank=True)
    due_date = models.DateTimeField('Fecha de vencimiento', null=True, blank=True)
    #Regresar una descripcion del incidente
    def __str__(self):
        return f"{self.incident_text} (by {self.user_creator} on {self.pub_date.strftime('%Y-%m-%d')})"
from markdownx.models import MarkdownxField
