from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import RegistroFormulario

def registro(request):
    if request.method == 'POST':
        formulario = RegistroFormulario(request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect('iniciar_sesion')  # 'iniciar_sesion'
    else:
        formulario = RegistroFormulario()
    return render(request, 'registro.html', {'formulario': formulario})

def iniciar_sesion(request):
    if request.method == 'POST':
        correo = request.POST['correo']
        password = request.POST['password']
        usuario = authenticate(request, correo=correo, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/admin/')  # Nota para Raul: Redirige a la página de admin, cambiala para que lleve a la info del usuario si quieres
        else:
            return render(request, 'iniciar_sesion.html', {'error': 'Credenciales incorrectas.'})
    return render(request, 'iniciar_sesion.html')
