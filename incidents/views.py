from django.http import JsonResponse  
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
import markdown
from django.utils.safestring import mark_safe
from .models import Incident
from organizaciones.models import Organizacion
from .forms import IncidentForm

class AddIncident(LoginRequiredMixin, generic.ListView):
    template_name = "incidents/add_incident.html"
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

            related_incident_id = request.POST.get('related_incident')
            if related_incident_id:
                related_incident = Incident.objects.get(id=related_incident_id)
                incident.related_incidents.add(related_incident)

            return redirect("incidents:add_incident", organizacion_id=self.organizacion_actual.id)
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
                "organizacion_id": self.organizacion_actual.id,
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
    template_name = 'incidents/detail.html'
    context_object_name = 'incident'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        description = context['incident'].description or ''
        context['incident'].description = mark_safe(markdown.markdown(description))
        context['organizacion_id'] = context['incident'].organizacion.id
        context['related_incidents'] = context['incident'].related_incidents.all()
        return context

class EditIncidentView(LoginRequiredMixin, generic.UpdateView):
    model = Incident
    template_name = "incidents/edit_incident.html"
    form_class = IncidentForm

    def get_queryset(self):
        return Incident.objects.filter(user_creator=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)

        related_incident_ids = self.request.POST.getlist('related_incidents')
        form.instance.related_incidents.set(related_incident_ids)

        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({"message": "Changes saved successfully!"})
        else:
            return response

    def get_success_url(self):
        return reverse('incidents:detail', args=[self.object.pk])  # Redirige a la vista de detalle en caso de solicitud normal
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        organizacion_id = self.kwargs.get('organizacion_id')
        context['organizacion_id'] = organizacion_id
        # Obtener todos los incidentes de la misma organización excepto el actual
        context['incidentes_organizacion'] = Incident.objects.filter(
            organizacion=self.object.organizacion
        ).exclude(id=self.object.id)
        return context

class IncidentTableView(LoginRequiredMixin, generic.ListView):
    model = Incident
    template_name = "incidents/table.html"
    context_object_name = "incidents"
    paginate_by = 10  # Implementamos paginación para mejorar la usabilidad

    def get(self, request, organizacion_id=None, *args, **kwargs):
        # Obtener la organización actual
        self.organizacion_actual = get_object_or_404(Organizacion, id=organizacion_id)
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
        
        if not self.request.user.is_superuser:
            # Si no es superusuario, mostramos solo los incidentes del usuario
            incidents = incidents.filter(user_creator=self.request.user)

        if user_creator:
            # Si se especifica, filtramos por creador de usuario
            incidents = incidents.filter(user_creator=user_creator)

        incidents = incidents.select_related('user_creator', 'organizacion')

        return incidents
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # organizacion_id = self.kwargs.get("organizacion_id")
        context["organizacion_id"] = self.organizacion_actual.id
        
         # Obtenemos la lista de usuarios que han creado incidentes en esta organización
        user_creators = (
            Incident.objects.filter(organizacion=self.organizacion_actual)
            .values_list('user_creator', flat=True)
            .distinct()
            .exclude
            (user_creator__isnull=True)
        )
        context['user_creators'] = user_creators
        return context
