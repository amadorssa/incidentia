from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from organizaciones.models import Organizacion

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
        ('REFACTORIZACIÓN', 'Refactorización'),
    ]
    ESTADO_CHOICES = [
        ('nuevo', 'Nuevo'),
        ('en_progreso', 'En progreso'),
        ('resuelto', 'Resuelto'),
        ('cerrado', 'Cerrado'),
        ('rechazado', 'Rechazado'),
    ]

    

    incident_text = models.CharField(max_length=200, null=True, blank=True)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="incidents", null=True, blank=True)
    # assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    user_creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    description = models.TextField(null=True, blank=True)
    prioridad = models.CharField(max_length=7, choices=PRIORIDAD_CHOICES, default='MEDIA')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, null=True, blank=True)
    attachment = models.FileField(upload_to='media/', null=True, blank=True)
    start_date = models.DateTimeField('Fecha de inicio', null=True, blank=True)
    due_date = models.DateTimeField('Fecha de vencimiento', null=True, blank=True)
    last_modified = models.DateTimeField('Última modificación', auto_now=True)
    related_incidents = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='nuevo')


    def clean(self):
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")

    def __str__(self):
        return f"{self.incident_text or 'Sin título'} (by {self.user_creator} on {self.pub_date.strftime('%Y-%m-%d')})"
