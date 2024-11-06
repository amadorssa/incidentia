from django.shortcuts import render, redirect, get_object_or_404
from .models import Organizacion, MiembroOrganizacion
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def crear_organizacion(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        organizacion = Organizacion.objects.create(nombre=nombre, correo=correo)
        MiembroOrganizacion.objects.create(usuario=request.user, organizacion=organizacion, rol=MiembroOrganizacion.ROL_ADMINISTRADOR)
        return redirect('perfil')
    return render(request, 'organizacion/crear_organizacion.html')

@login_required
def unirse_organizacion(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        organizacion = get_object_or_404(Organizacion, codigo_acceso=codigo)
        miembro, created = MiembroOrganizacion.objects.get_or_create(usuario=request.user, organizacion=organizacion, rol=MiembroOrganizacion.ROL_USUARIO)
        if created:
            messages.success(request, "Te has unido a la organización.")
        else:
            messages.warning(request, "Ya eres miembro de esta organización.")
        return redirect('perfil')
    return render(request, 'organizacion/unirse_organizacion.html')

@login_required
def mis_organizaciones(request):
    # Obtener las organizaciones en las que el usuario es miembro
    organizaciones = MiembroOrganizacion.objects.filter(usuario=request.user)
    return render(request, 'organizacion/mis_organizaciones.html', {'organizaciones': organizaciones})


#@login_required
#def ver_organizacion(request, organizacion_id):
#    organizacion = get_object_or_404(Organizacion, id=organizacion_id)
#    miembros = organizacion.miembros.all()
#    
#    # Redirigir a la página de incidentes de la organización
#    return redirect('incidents:index', organizacion_id=organizacion.id)

@login_required
def ver_organizacion(request, organizacion_id):
    organizacion = get_object_or_404(Organizacion, id=organizacion_id)
    if not organizacion.miembros.filter(usuario=request.user).exists():
        return redirect('mis_organizaciones')
    miembros = organizacion.miembros.all()
    return render(request, 'organizacion/ver_organizacion.html', {'organizacion': organizacion, 'miembros': miembros})
