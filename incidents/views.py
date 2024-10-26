from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse
from django.db.models import Q
import markdown

from .forms import IncidentForm
from .models import Incident

@method_decorator(login_required, name='dispatch') 
class IndexView(generic.ListView):
    template_name = "incidents/index.html"

    def get(self, request, *args, **kwargs):
        """Mostrar el formulario usando GET requests."""
        form = IncidentForm()
        return self.render_form(form)

    def post(self, request, *args, **kwargs):
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo incidente
            return redirect("incidents:index")  # Redirecciona al index
        return self.get(request, *args, **kwargs)  # Si no es válido, muestra el formulario

    def render_form(self, form):
        """Funcion para hacer render del formulario"""
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context={"form": form},
        )

    context_object_name = "latest_incident_list"

    def get_queryset(self):
        """Return the last five published incidents."""
        return Incident.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IncidentForm()  # Añadir el formulario al contexto
        return context

    def post(self, request, *args, **kwargs):
        form = IncidentForm(request.POST, request.FILES)  # Añadir request.FILES para manejar archivos
        if form.is_valid():
            form.save()  # Guarda el nuevo incidente junto con el archivo
            return redirect("incidents:index")  # Redirecciona al index
        return self.get(request, *args, **kwargs)  # Si no es válido, muestra el formulario

@method_decorator(login_required, name='dispatch') 
class DetailView(generic.DetailView):
    model = Incident
    template_name = 'incidents/detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Convertir la descripción de Markdown a HTML
        context['incident'].description = markdown.markdown(context['incident'].description)
        return context

@method_decorator(login_required, name='dispatch') 
class EditIncidentView(generic.UpdateView):
    model = Incident
    template_name = "incidents/edit_incident.html"
    form_class = IncidentForm

    def get_success_url(self):
        return reverse('incidents:detail', args=[self.object.pk])  # Redirecciona a la vista de detalle después de guardar
    
@method_decorator(login_required, name='dispatch') 
class IncidentTableView(generic.ListView):
    model = Incident
    template_name = "incidents/table.html"
    context_object_name = "incidents"

    def get_queryset(self):
        """Regresar todos los incidentes por fecha mas reciente."""
        query = self.request.GET.get("q", "")
        user_creator = self.request.GET.get("user_creator", "")

        incidents = Incident.objects.filter(
            Q(incident_text__icontains=query)
        )

        # Filtar por usuario seleccionado
        if user_creator:
            incidents = incidents.filter(user_creator=user_creator)

        # Ordenar por fecha de publicacion mas reciente
        incidents = incidents.order_by("-pub_date")
        # Convertir la descripcion a tipo Markdown para cada incidente
        for incident in incidents:
            incident.description = markdown.markdown(incident.description or '')

        return incidents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_creators = ( Incident.objects.values_list('user_creator', flat=True)
                        .distinct()
                        .exclude(user_creator__isnull=True))

        context['user_creators'] = user_creators
        return context
