from django import forms
from .models import Usuario

class RegistroFormulario(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['correo', 'nombre', 'apellido', 'password']

    def clean_password(self):
        return self.cleaned_data['password']

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data['password'])
        if commit:
            usuario.save()
        return usuario
