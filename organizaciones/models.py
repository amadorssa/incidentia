from django.db import models
from django.conf import settings
import random
import string

class Organizacion(models.Model):
    nombre = models.CharField(max_length=255, unique=True)
    correo = models.EmailField()
    codigo_acceso = models.CharField(max_length=10, unique=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.codigo_acceso:
            self.codigo_acceso = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

class MiembroOrganizacion(models.Model):
    ROL_ADMINISTRADOR = 'ADMINISTRADOR'
    ROL_USUARIO = 'USUARIO'
    ROLES = [
        (ROL_ADMINISTRADOR, 'Administrador'),
        (ROL_USUARIO, 'Usuario'),
    ]

    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.CASCADE, related_name="miembros")
    rol = models.CharField(max_length=20, choices=ROLES)

    class Meta:
        unique_together = ('usuario', 'organizacion')

    def __str__(self):
        return f"{self.usuario.username} - {self.organizacion.nombre} ({self.rol})"

