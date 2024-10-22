import datetime
from django.db import models
from django.utils import timezone
from markdownx.models import MarkdownxField

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
    prioridad = models.CharField(max_length=7, choices=PRIORIDAD_CHOICES, default='MEDIA')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = MarkdownxField(null=True, blank=True)  # Campo de descripción con soporte Markdown
    attachment = models.FileField(upload_to='media/', null=True, blank=True)  # Subir archivos opcional


    def __str__(self):
        return self.incident_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
