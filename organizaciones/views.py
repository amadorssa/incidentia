from django.shortcuts import render, redirect, get_object_or_404
from .models import Organizacion, MiembroOrganizacion
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def create_organization(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        organizacion = Organizacion.objects.create(nombre=nombre, correo=correo)
        MiembroOrganizacion.objects.create(usuario=request.user, organizacion=organizacion, rol=MiembroOrganizacion.ROL_ADMINISTRADOR)
        return redirect('profile')
    return render(request, 'create_organization.html')

@login_required
def join_organization(request):
    if request.method == "POST":
        codigo = request.POST.get('codigo')
        organizacion = get_object_or_404(Organizacion, codigo_acceso=codigo)
        miembro, created = MiembroOrganizacion.objects.get_or_create(usuario=request.user, organizacion=organizacion, rol=MiembroOrganizacion.ROL_USUARIO)
        if created:
            messages.success(request, "Te has unido a la organización.")
        else:
            messages.warning(request, "Ya eres miembro de esta organización.")
        return redirect('profile')
    return render(request, 'join_organization.html')

@login_required
def my_organizations(request):
    # Obtener las organizaciones en las que el usuario es miembro
    organizaciones = MiembroOrganizacion.objects.filter(usuario=request.user)
    return render(request, 'my_organizations.html', {'organizaciones': organizaciones})

@login_required
# def ver_organizacion(request, organizacion_id):
def organization_detail(request, slug):
    # organizacion = get_object_or_404(Organizacion, id=organizacion_id)
    organizacion = get_object_or_404(Organizacion, slug=slug)
    if not organizacion.miembros.filter(usuario=request.user).exists():
        return redirect('my_organizations')
    miembros = organizacion.miembros.all()
    return render(request, 'organization_detail.html', {'organizacion': organizacion, 'miembros': miembros})
