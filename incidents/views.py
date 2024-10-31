from django.http import JsonResponse  
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from .models import Incident, Organizacion
import markdown

from .forms import IncidentForm
from .models import Incident

class IndexView(generic.ListView):
    template_name = "incidents/index.html"
    context_object_name = "latest_incident_list"

    def get(self, request, organizacion_id=None, *args, **kwargs):
        # Obtener la organización actual
        self.organizacion_actual = get_object_or_404(Organizacion, id=organizacion_id)
        form = IncidentForm()
        return self.render_form(form)

    def post(self, request, organizacion_id=None, *args, **kwargs):
        self.organizacion_actual = get_object_or_404(Organizacion, id=organizacion_id)
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            incident = form.save(commit=False)
            incident.user_creator = request.user
            incident.organizacion = self.organizacion_actual  # Asocia el incidente con la organización
            incident.save()
            return redirect("incidents:index", organizacion_id=organizacion_id)
        return self.render_form(form)

    def render_form(self, form):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context={
                "form": form,
                "latest_incident_list": self.get_queryset(),
                "organizacion_id": self.organizacion_actual.id  # Agrega el ID de la organización
            },
        )

    def get_queryset(self):
        return Incident.objects.filter(
            user_creator=self.request.user, 
            organizacion=self.organizacion_actual  # Filtra por la organización actual
        ).order_by("-pub_date")[:5]




@method_decorator(login_required, name='dispatch') 
class DetailView(generic.DetailView):
    model = Incident
    template_name = 'incidents/detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Convertir la descripción de Markdown a HTML
        context['incident'].description = markdown.markdown(context['incident'].description)
        # Obtener la organización a la que pertenece el incidente
        context['organizacion_id'] = context['incident'].organizacion.id  # Agrega el ID de la organización
        return context

@method_decorator(login_required, name='dispatch') 
class EditIncidentView(generic.UpdateView):
    model = Incident
    template_name = "incidents/edit_incident.html"
    form_class = IncidentForm

    def form_valid(self, form):
        self.object = form.save()
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':  # Verifica si la solicitud es AJAX
            return JsonResponse({"message": "Changes saved successfully!"})
        return super().form_valid(form)  # Si no es AJAX, procede con el flujo normal

    def get_success_url(self):
        return reverse('incidents:detail', args=[self.object.pk])  # Redirige a la vista de detalle en caso de solicitud normal
    
@method_decorator(login_required, name='dispatch')
class IncidentTableView(generic.ListView):
    model = Incident
    template_name = "incidents/table.html"
    context_object_name = "incidents"

    def get_queryset(self):
        """Regresar todos los incidentes por fecha más reciente para el usuario autenticado."""
        query = self.request.GET.get("q", "")
        user_creator = self.request.GET.get("user_creator")
        
        # Filtra los incidentes basándose en el usuario y el parámetro de búsqueda
        incidents = Incident.objects.filter(
            user_creator=self.request.user,
            incident_text__icontains=query,
        ).order_by("-pub_date")
        
        if user_creator:
            incidents = incidents.filter(user_creator=user_creator)

        # Convierte la descripción a tipo Markdown para cada incidente
        for incident in incidents:
            incident.description = markdown.markdown(incident.description or '')

        return incidents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene el ID de la organización desde los argumentos de la URL
        organizacion_id = self.kwargs.get("organizacion_id")
        context['organizacion_id'] = organizacion_id
        
        # Obtiene los usuarios que crearon incidentes (opcional)
        user_creators = (
            Incident.objects.values_list('user_creator', flat=True)
            .distinct()
            .exclude(user_creator__isnull=True)
        )
        context['user_creators'] = user_creators
        return context
