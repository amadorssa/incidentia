from django.shortcuts import render, redirect, get_object_or_404
from .models import Organizacion, MiembroOrganizacion
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def create_organization(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        correo = request.POST.get('correo')
        organizacion = Organizacion.objects.create(nombre=nombre, correo=correo)
        MiembroOrganizacion.objects.create(usuario=request.user, organizacion=organizacion, rol=MiembroOrganizacion.ROL_ADMINISTRADOR)
        return redirect('my_organizations')
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
        return redirect('my_organizations')
    return render(request, 'join_organization.html')

@login_required
def my_organizations(request):
    # Obtener las organizaciones en las que el usuario es miembro
    organizaciones = MiembroOrganizacion.objects.filter(usuario=request.user)
    return render(request, 'my_organizations.html', {'organizaciones': organizaciones})

@login_required
def organization_detail(request, slug):
    organizacion = get_object_or_404(Organizacion, slug=slug)
    user_member = organizacion.miembros.filter(usuario=request.user).first()
    if not organizacion.miembros.filter(usuario=request.user).exists():
        return redirect('my_organizations')
    # Checar si usuario es admin para mostrar boton de eliminado.
    is_admin = user_member.rol == MiembroOrganizacion.ROL_ADMINISTRADOR
    miembros = organizacion.miembros.all()

    if request.method == "POST" and is_admin:
        usuario_id = request.POST.get("usuario_id")
        nuevo_rol = request.POST.get("rol")
        miembro = get_object_or_404(MiembroOrganizacion, usuario_id=usuario_id, organizacion=organizacion)
        
        # Permitir solo la actualización a administrador o usuario
        if nuevo_rol in dict(MiembroOrganizacion.ROLES).keys():
            miembro.rol = nuevo_rol
            miembro.save()
            messages.success(request, f"El rol de {miembro.usuario.nombre} ha sido actualizado a {nuevo_rol}.")
        else:
            messages.error(request, "Rol inválido.")
        return redirect("organization_detail", slug=slug)


    return render(request, 'organization_detail.html', {'organizacion': organizacion, 'miembros': miembros, 'is_admin': is_admin})

@login_required
def delete_user(request, slug, usuario_id):
    """Vista para permitir la eliminacion de un usuario de la organizacion"""
    organizacion = get_object_or_404(Organizacion, slug=slug)
    miembro = get_object_or_404(MiembroOrganizacion, usuario_id=usuario_id, organizacion=organizacion)
    miembro.delete()
    messages.success(request, "Usuario borrado satisfactoriamente.")
    return redirect(f"{reverse('organization_detail', args=[slug])}")
    
