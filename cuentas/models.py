from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    foto_perfil = models.TextField(blank=True, null=True)  # Para almacenar la URL o ruta de la imagen (el ImageField daba problemas por culpa de Pillow)

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

