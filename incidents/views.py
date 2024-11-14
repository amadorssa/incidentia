from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
import markdown
from django.utils.safestring import mark_safe
from .models import Incident
from organizaciones.models import Organizacion, MiembroOrganizacion
from .forms import IncidentForm
import csv
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class AddIncident(LoginRequiredMixin, generic.View):
    template_name = "add_incident.html"

    def get(self, request, slug=None, *args, **kwargs):
        self.organizacion_actual = get_object_or_404(Organizacion, slug=slug)
        form = IncidentForm()
        return self.render_form(form)

    def post(self, request, slug=None, *args, **kwargs):
        self.organizacion_actual = get_object_or_404(Organizacion, slug=slug)
        form = IncidentForm(request.POST, request.FILES)

        if form.is_valid():
            incident = form.save(commit=False)
            incident.user_creator = request.user
            incident.organizacion = self.organizacion_actual
            incident.save()

            related_incident_id = request.POST.get('related_incident')
            if related_incident_id:
                try:
                    related_incident = Incident.objects.get(id=related_incident_id)
                    incident.related_incidents.add(related_incident)
                except Incident.DoesNotExist:
                    print("El incidente relacionado no existe")

            return redirect("incidents:add_incident", slug=self.organizacion_actual.slug)
        else:
            print(form.errors)  # Imprime los errores en la consola para depuración
        return self.render_form(form)

    def render_form(self, form):
        return render(
            request=self.request,
            template_name=self.template_name,
            context={
                "form": form,
                "latest_incident_list": self.get_queryset(),
                "slug": self.organizacion_actual.slug,
                "incidentes_organizacion": Incident.objects.filter(organizacion=self.organizacion_actual),
            },
        )

    def get_queryset(self):
        return Incident.objects.filter(
            user_creator=self.request.user, 
            organizacion=self.organizacion_actual  # Filtra por la organización actual
        ).order_by("-pub_date")[:5]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Incident
    template_name = 'detail.html'
    context_object_name = 'incident'

    def get(self, request, slug=None, *args, **kwargs):
        # Obtener la organización actual
        self.organizacion_actual = get_object_or_404(Organizacion, slug=slug)
        # Checa si el usuario es admin de organizacion
        self.user_member = MiembroOrganizacion.objects.filter(
            organizacion = self.organizacion_actual,
            usuario = request.user
        ).first()
        self.is_admin = self.user_member and self.user_member.rol == MiembroOrganizacion.ROL_ADMINISTRADOR
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        description = context['incident'].description or ''
        context['incident'].description = mark_safe(markdown.markdown(description))
        context['slug'] = context['incident'].organizacion.slug
        context['related_incidents'] = context['incident'].related_incidents.all()
        context["is_admin"] = self.is_admin
        return context

class EditIncidentView(LoginRequiredMixin, generic.UpdateView):
    model = Incident
    template_name = "edit_incident.html"
    form_class = IncidentForm

    def get_queryset(self):
        #return Incident.objects.filter(user_creator=self.request.user)
        # Solo el admin y creador de incidente puede editar
        user = self.request.user
        creator_incidents = Incident.objects.filter(user_creator=user)
        admin_organizations = MiembroOrganizacion.objects.filter(
            usuario = user,
            rol='ADMINISTRADOR'
        ).values_list('organizacion', flat=True)

        admin_incidents = Incident.objects.filter(organizacion__in=admin_organizations)
        return creator_incidents | admin_incidents

    def form_valid(self, form):
        response = super().form_valid(form)

        # related_incident_ids = self.request.POST.get('related_incidents', '').split(',')
        related_incident_ids = [id for id in self.request.POST.get('related_incidents', '').split(',') if id]

        if related_incident_ids:
            form.instance.related_incidents.set(related_incident_ids)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"message": "Changes saved successfully!"})
        else:
            return response

    def get_success_url(self):
        return reverse('incidents:detail', kwargs={'slug': self.object.organizacion.slug, 'pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        context['incidentes_organizacion'] = Incident.objects.filter(
            organizacion=self.object.organizacion
        ).exclude(id=self.object.id)
        return context

class IncidentTableView(LoginRequiredMixin, generic.ListView):
    model = Incident
    template_name = "table.html"
    context_object_name = "incidents"

    def get(self, request, slug=None, *args, **kwargs):
        # Obtener la organización actual
        self.organizacion_actual = get_object_or_404(Organizacion, slug=slug)
        # Checa si el usuario es admin de organizacion
        self.user_member = MiembroOrganizacion.objects.filter(
            organizacion = self.organizacion_actual,
            usuario = request.user
        ).first()
        self.is_admin = self.user_member and self.user_member.rol == MiembroOrganizacion.ROL_ADMINISTRADOR
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        ordering = self.request.GET.get("ordering", "-pub_date")
        user_creator = self.request.GET.get("user_creator")
        
        # Filtramos por organización y texto de búsqueda
        incidents = Incident.objects.filter(
            organizacion=self.organizacion_actual,
            incident_text__icontains=query,
        ).order_by(ordering)

        # MUESTRA TODOS LOS INCIDENTES SI SUPER USUARIO
#       Cambio de superusuario por admin
#        if not self.request.user.is_superuser:
#            # Si no es superusuario, mostramos solo los incidentes del usuario
#            incidents = incidents.filter(user_creator=self.request.user)

        # MUESTRA TODOS LOS INCIDENTES SI ADMIN
        #if not self.is_admin:
            # Si no es admin, mostramos solo los incidentes del usuario
        #    incidents = incidents.filter(user_creator=self.request.user)
        #if user_creator:
        #    # Si se especifica, filtramos por creador de usuario
        #    incidents = incidents.filter(user_creator=user_creator)

        if user_creator:
            incidents = incidents.filter(user_creator=user_creator)

        incidents = incidents.select_related('user_creator', 'organizacion')

        return incidents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # slug = self.kwargs.get("slug")
        context["slug"] = self.organizacion_actual.slug
        context["is_admin"] = self.is_admin
        
         # Obtenemos la lista de usuarios que han creado incidentes en esta organización
         # Usando ID y objeto User para obtener el nombre de los usuarios
        User = get_user_model()
        user_ids = (
            Incident.objects.filter(organizacion=self.organizacion_actual)
            .values_list('user_creator', flat=True)
            .distinct()
            .exclude
            (user_creator__isnull=True)
        )
        user_creators = User.objects.filter(id__in=user_ids)

        incidents = self.get_queryset()
        paginator = Paginator(incidents, 10)
        page = self.request.GET.get('page')

        #Intenta paginar los incidentes si son mas de 10
            #Muestra la primer pagina si no es un entero
            #Muestra la ultima pagina si esta fuera de rango
        try:
            paginated_incidents = paginator.page(page)
        except PageNotAnInteger:
            paginated_incidents = paginator.page(1) 
        except EmptyPage:
            paginated_incidents = paginator.page(paginator.num_pages)

        context['incidents'] = paginated_incidents
        context['user_creators'] = user_creators
        return context

def delete_incident(request, slug, pk):
    """Vista para permitir la eliminacion de un incidente de la base de datos"""
    organizacion = get_object_or_404(Organizacion, slug=slug)
    incident = get_object_or_404(Incident, pk=pk, organizacion=organizacion)

    incident.delete()
    messages.success(request, "Incidente borrado satisfactoriamente.")
    page = request.GET.get('page', 1)
    return redirect(f"{reverse('incidents:incident_table', args=[slug])}?page={page}")

def export_incidents_csv(request, slug):
    """Vista para permitir descargar la tabla filtrada"""
    organizacion = get_object_or_404(Organizacion, slug=slug)
    query = request.GET.get('q')
    user_creator = request.GET.get('user_creator')

    #Obtener los incidentes que se exportaran con o sin filtros
    incidents = Incident.objects.filter(
            organizacion=organizacion,
            incident_text__icontains=query,
    ).order_by("-pub_date")
        
    if user_creator:
        incidents = incidents.filter(user_creator=user_creator)

    #Crear el archivo CSV 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="tabla_filtrada.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Incidente', 'Usuario', 'Descripcion', 'Prioridad', 'Categoría',
                     'Fecha Inicio', 'Fecha Vencimiento', 'Fecha Publicacion']) #Nombre de columnas

    #Llenar response con los incidentes
    for incident in incidents:
        writer.writerow([incident.id, incident.incident_text, str(incident.user_creator),
                         incident.description, incident.prioridad, incident.category, incident.start_date,
                         incident.due_date, incident.pub_date])

    return response

def generate_pdf(request, slug, pk):
    """Vista para permitir la generacion de un incidente en formato PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="document.pdf"'
    organizacion = get_object_or_404(Organizacion, slug=slug)
    incident = get_object_or_404(Incident, pk=pk, organizacion=organizacion)

    organizacion_nombre = organizacion.nombre
    # Usar diccionario para imprimir detalles
    # Attachment y Related still missing
    data = {"Incidente": incident.incident_text, "Creador": str(incident.user_creator),
            "Descripción": incident.description, "Fecha Inicio": incident.start_date, "Fecha Vencimiento": incident.due_date, 
            "Fecha Publicación": incident.pub_date, "Prioridad": incident.prioridad, "Categoria": incident.category,
            "Incidentes Relacionados": [f'{related.incident_text}'
                                        for related in incident.related_incidents.all()] if incident.related_incidents.exists() else "Ninguno",
            "Ultima Modificación": incident.last_modified, "Archivo Adjunto": (f'<a href="{incident.attachment.url}" download>Archivo</a>' if incident.attachment else "Ninguno")}

    # Crear el canvas
    p = canvas.Canvas(response, pagesize=letter)

    # Titulo reporte y separaciones
    p.setFont("Helvetica-Bold", 18, leading=None)
    p.drawString(40, 750, f"Reporte Incidente #{incident.id} - Organización: {organizacion_nombre}")
    p.line(0, 740, 1000, 740)
    p.setFillColorRGB(0.769, 0.008, 0.008)
    p.line(0, 738, 1000, 738)
    p.setFillColorRGB(0, 0, 0)
    xl = 20
    yl = 700
    zl = 15

    # Renderizar data de incidente
    for t, v in data.items():
        p.setFont("Helvetica-Bold", 15, leading=None)
        p.drawString(xl, yl, f"{t}")
        p.setFont("Helvetica", 12, leading=None)
        p.drawString(xl+zl, yl-zl, f"{v}")
        yl -= 40

    p.setTitle(f'Reporte Incidente #{incident.id}')
    # Guardar PDF
    p.showPage()
    p.save()

    return response