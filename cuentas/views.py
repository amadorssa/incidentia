from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .forms import RegistroFormulario, PerfilFormulario, CambiarPassFormulario
from .models import Usuario, UsuarioManager

def sign_up(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        formulario = RegistroFormulario(request.POST)

        correo = request.POST.get('correo')  # Obtiene el correo del formulario

        # Validar si el correo ya está registrado
        if Usuario.objects.filter(correo=correo).exists():
            messages.error(request, "Ya existe una cuenta registrada con este correo. Inicia sesión.")
            return redirect('accounts:sign_in')  # Redirige a la página de inicio de sesión


        if formulario.is_valid():
            formulario.save()
            return redirect('accounts:sign_in')
        else:
            messages.error(request, "Error en el registro. Inténtalo de nuevo.")
    else:
        formulario = RegistroFormulario()
    return render(request, 'signup.html', {'formulario': formulario})

def sign_in(request):
    if request.user.is_authenticated:
        messages.info(request, "Ya has iniciado sesión.")
        return redirect('accounts:profile')

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
    return redirect('accounts:sign_in')

@login_required
def edit_profile(request, slug):
    usuario = request.user  # Obtiene el usuario actualmente autenticado
    if request.method == 'POST':
        formulario = PerfilFormulario(request.POST, request.FILES, instance=usuario)  # Incluir request.FILES para manejar archivos
        if formulario.is_valid():
            formulario.save()
            return redirect('accounts:profile', slug=slug)  # Redirige al perfil actualizado
    else:
        formulario = PerfilFormulario(instance=usuario)

    return render(request, 'edit_profile.html', {'formulario': formulario, 'usuario': usuario, 'slug': slug})

@login_required
def profile(request, slug):
    usuario = request.user    
    return render(request, 'profile.html', {'usuario': usuario, 'slug': slug})

@login_required
def change_pass(request, slug):
    if request.method == 'POST':
        formulario = CambiarPassFormulario(request.user, request.POST)

        if formulario.is_valid():
            new_pass = formulario.cleaned_data['new_pass']
            request.user.set_password(new_pass)
            request.user.save()
            # Mantener sesion iniciada despues de cambio contrasena
            update_session_auth_hash(request, request.user)
            messages.success(request, "Contraseña cambiada satisfactoriamente.")
            return redirect('accounts:profile', slug=slug)
    else:
        formulario = CambiarPassFormulario(request.user)
    return render(request, 'change_pass.html', {'formulario': formulario, 'slug': slug})



