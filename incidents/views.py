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
    context_object_name = "latest_incident_list"

    def get(self, request, *args, **kwargs):
        form = IncidentForm()
        return self.render_form(form)

    def post(self, request, *args, **kwargs):
        form = IncidentForm(request.POST, request.FILES)
        if form.is_valid():
            # Asocia el incidente con el usuario autenticado antes de guardarlo
            incident = form.save(commit=False)
            incident.user_creator = request.user
            incident.save()
            return redirect("incidents:index")
        return self.render_form(form)

    def render_form(self, form):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context={"form": form, "latest_incident_list": self.get_queryset()},
        )

    def get_queryset(self):
        # Filtra los incidentes solo para el usuario autenticado
        return Incident.objects.filter(user_creator=self.request.user).order_by("-pub_date")[:5]

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
        """Regresar todos los incidentes por fecha más reciente para el usuario autenticado."""
        query = self.request.GET.get("q", "")

        incidents = Incident.objects.filter(
            user_creator=self.request.user,  # Filtra por el usuario autenticado
            incident_text__icontains=query
        ).order_by("-pub_date")

        # Convertir la descripción a tipo Markdown para cada incidente
        for incident in incidents:
            incident.description = markdown.markdown(incident.description or '')

        return incidents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtiene solo los nombres de usuario del usuario autenticado
        context['user_creators'] = [self.request.user]
        return context

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_creators = ( Incident.objects.values_list('user_creator', flat=True)
                        .distinct()
                        .exclude(user_creator__isnull=True))

        context['user_creators'] = user_creators
        return context
