from django import forms
from .models import Usuario
from django.core.exceptions import ValidationError

class RegistroFormulario(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,  # Esto oculta la contraseña
        label="Contraseña"
    )

    class Meta:
        model = Usuario
        fields = ['correo', 'nombre', 'apellido', 'password']

    def clean_password(self):
        return self.cleaned_data['password']
    
        # # Validaciones de la contraseña
        # if len(password) < 8:
        #     raise ValidationError("La contraseña debe tener al menos 8 caracteres.")
        # if not re.search(r"\d", password):
        #     raise ValidationError("La contraseña debe incluir al menos un número.")
        # if not re.search(r"[A-Z]", password):
        #     raise ValidationError("La contraseña debe incluir al menos una letra mayúscula.")
        # if not re.search(r"[a-z]", password):
        #     raise ValidationError("La contraseña debe incluir al menos una letra minúscula.")
        # if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        #     raise ValidationError("La contraseña debe incluir al menos un carácter especial (e.g., !@#$%^&*).")

        return password


    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario
    
class PerfilFormulario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'foto_perfil', 'correo']

    # Permitir la subida de imágenes
    def __init__(self, *args, **kwargs):
        super(PerfilFormulario, self).__init__(*args, **kwargs)
        self.fields['foto_perfil'].required = False  # la foto no sea obligatoria
        self.fields['foto_perfil'].widget.attrs.update({'class': 'custom-file-input'})
        # Hacer que el campo 'correo' sea de solo lectura
        self.fields['correo'].widget.attrs['readonly'] = True


    def clean_foto_perfil(self):
        foto = self.cleaned_data.get('foto_perfil')

        # Verificar si se ha subido una imagen
        if foto:
            # Validar el tipo de archivo
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            extension = foto.name.split('.')[-1].lower()
            if extension not in valid_extensions:
                raise ValidationError("Formato no permitido. Solo se permiten archivos JPEG, PNG y GIF.")

            # Validar el tamaño de la imagen (máximo 5 MB)
            if foto.size > 5 * 1024 * 1024:  # 5 MB en bytes
                raise ValidationError("El tamaño máximo permitido para la imagen es de 5 MB.")

        return foto

