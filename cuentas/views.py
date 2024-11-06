from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import RegistroFormulario, PerfilFormulario
from .models import Usuario, UsuarioManager

def registro(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('perfil')

    if request.method == 'POST':
        formulario = RegistroFormulario(request.POST)

        correo = request.POST.get('correo')  # Obtiene el correo del formulario

        # Validar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists() or UsuarioManager.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe una cuenta registrada con este correo. Inicia sesión.")
            return redirect('iniciar_sesion')  # Redirige a la página de inicio de sesión


        if formulario.is_valid():
            formulario.save()
            return redirect('iniciar_sesion')
        else:
            messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        formulario = RegistroFormulario()
    return render(request, 'registro.html', {'formulario': formulario})

def iniciar_sesion(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('perfil')

    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        usuario = authenticate(request, correo=correo, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/organizaciones/mis-organizaciones/')  # Nota para Raul: Redirige a la página de admin, cambiala para que 
                                        #lleve a la info del usuario si quieres
        else:
            return render(request, 'iniciar_sesion.html', {'error': 'Credenciales incorrectas.'})
    return render(request, 'iniciar_sesion.html')


#LOGOUT
def cerrar_sesion(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('iniciar_sesion')

@login_required
def perfil(request):
    usuario = request.user  # Obtiene el usuario actualmente autenticado
    if request.method == 'POST':
        formulario = PerfilFormulario(request.POST, request.FILES, instance=usuario)  # Incluir request.FILES para manejar archivos
        if formulario.is_valid():
            formulario.save()
            return redirect('perfil')  # Redirige al perfil actualizado
    else:
        formulario = PerfilFormulario(instance=usuario)

    return render(request, 'perfil.html', {'formulario': formulario, 'usuario': usuario})



