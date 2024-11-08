from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from organizaciones.models import Organizacion


class UsuarioManager(BaseUserManager):
    def create_user(self, correo, nombre, apellido, password=None, **extra_fields):
        if not correo:
            raise ValueError('El usuario debe tener un correo electrónico')
        
        correo = self.normalize_email(correo)
        user = self.model(correo=correo, nombre=nombre, apellido=apellido, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo, nombre, apellido, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(correo, nombre, apellido, password, **extra_fields)

class Usuario(AbstractUser):
    username = None 
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    foto_perfil = models.FileField(upload_to='perfil/', blank=True, null=True) # Para almacenar la URL o ruta de la imagen (el ImageField daba problemas por culpa de Pillow)
    organizacion = models.ForeignKey(Organizacion, on_delete=models.SET_NULL, null=True, blank=True)  # Relación opcional con Organizacion


    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    objects = UsuarioManager()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

