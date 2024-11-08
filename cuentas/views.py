from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import RegistroFormulario, PerfilFormulario
from .models import Usuario, UsuarioManager

def sign_up(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('profile')

    if request.method == 'POST':
        formulario = RegistroFormulario(request.POST)

        correo = request.POST.get('correo')  # Obtiene el correo del formulario

        # Validar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe una cuenta registrada con este correo. Inicia sesión.")
            return redirect('sign_in')  # Redirige a la página de inicio de sesión


        if formulario.is_valid():
            formulario.save()
            return redirect('sign_in')
        else:
            messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        formulario = RegistroFormulario()
    return render(request, 'signup.html', {'formulario': formulario})

def sign_in(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('profile')

    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        usuario = authenticate(request, correo=correo, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('my_organizations')
        else:
            return render(request, 'login.html', {'error': 'Credenciales incorrectas.'})
    return render(request, 'login.html')


#LOGOUT
def sign_out(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('sign_in')

@login_required
def edit_profile(request):
    usuario = request.user  # Obtiene el usuario actualmente autenticado
    if request.method == 'POST':
        formulario = PerfilFormulario(request.POST, request.FILES, instance=usuario)  # Incluir request.FILES para manejar archivos
        if formulario.is_valid():
            formulario.save()
            return redirect('profile')  # Redirige al perfil actualizado
    else:
        formulario = PerfilFormulario(instance=usuario)

    return render(request, 'edit_profile.html', {'formulario': formulario, 'usuario': usuario})

@login_required
def profile(request):
    usuario = request.user
    return render(request, 'profile.html', {'usuario': usuario})



