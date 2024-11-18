from django.db import models
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from organizaciones.models import MiembroOrganizacion, Organizacion
from cuentas.models import Usuario


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

    incident_text = models.CharField(max_length=200, default='')
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="incidents", null=True, blank=True)
    assigned_to = models.ForeignKey(MiembroOrganizacion, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_incidents')
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
    usuario_modificador = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='modified_incidents')


    def clean(self):
        if self.start_date and self.due_date and self.start_date > self.due_date:
            raise ValidationError("La fecha de inicio no puede ser posterior a la fecha de vencimiento.")
        
        if self.assigned_to and self.organizacion and self.assigned_to.organizacion != self.organizacion:
            raise ValidationError("El usuario asignado debe pertenecer a la organización del incidente.")
        

    def save(self, *args, **kwargs):
        if self.pk:  # Solo registra cambios si el objeto ya existe
            incidente_anterior = Incident.objects.get(pk=self.pk)
            cambios = []

            for campo in self._meta.fields:
                campo_nombre = campo.name
                valor_nuevo = getattr(self, campo_nombre)
                valor_anterior = getattr(incidente_anterior, campo_nombre)

                if valor_nuevo != valor_anterior:
                    cambios.append(campo_nombre)

            if cambios:
                HistorialIncidente.objects.create(
                    incidente=self,
                    usuario=self.usuario_modificador,
                    campos_modificados=cambios,
                )

        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.incident_text or 'Sin título'} (by {self.user_creator} on {self.pub_date.strftime('%Y-%m-%d')})"
    
class HistorialIncidente(models.Model):
    incidente = models.ForeignKey(
        Incident, on_delete=models.CASCADE, related_name='historial')
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    fecha = models.DateTimeField(auto_now_add=True)
    campos_modificados = models.JSONField()  # Guarda los nombres de los campos modificados en formato JSON.

    def __str__(self):
        return f"Historial para incidente {self.incidente.id} por {self.usuario.nombre} {self.usuario.apellido if self.usuario else 'Desconocido'}"