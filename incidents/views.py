from django.http import JsonResponse  
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import generic
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Incident, Organizacion, Attachment
from .forms import IncidentForm, AttachmentFormSet
from django.contrib.auth.mixins import LoginRequiredMixin  # Import LoginRequiredMixin
from django.views.generic import UpdateView, View
from django.contrib import messages
import markdown

from .forms import IncidentForm
from .models import Incident

class IndexView(LoginRequiredMixin, generic.ListView):
    model = Incident
    template_name = "incidents/index.html"
    context_object_name = "latest_incident_list"

    def get(self, request, organizacion_id=None, *args, **kwargs):
        # Obtener la organización actual
        self.organizacion_actual = get_object_or_404(Organizacion, id=organizacion_id)
        form = IncidentForm()
        attachment_formset = AttachmentFormSet()
        return self.render_form(form, attachment_formset)

    def post(self, request, organizacion_id=None, *args, **kwargs):
        self.organizacion_actual = get_object_or_404(Organizacion, id=organizacion_id)
        form = IncidentForm(request.POST, request.FILES)
        attachment_formset = AttachmentFormSet(request.POST, request.FILES)
        if form.is_valid() and attachment_formset.is_valid():
            incident = form.save(commit=False)
            incident.user_creator = request.user
            incident.organizacion = self.organizacion_actual
            incident.save()
            attachment_formset.instance = incident
            attachment_formset.save()
            return redirect("incidents:index", organizacion_id=organizacion_id)
        else:
            return self.render_form(form, attachment_formset)

    def render_form(self, form, attachment_formset):
        return self.response_class(
            request=self.request,
            template=self.template_name,
            context={
                "form": form,
                "attachment_formset": attachment_formset,  # attachment_formset is not defined here
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
class EditIncidentView(LoginRequiredMixin, UpdateView):
    model = Incident
    template_name = "incidents/edit_incident.html"
    form_class = IncidentForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['attachment_formset'] = AttachmentFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['attachment_formset'] = AttachmentFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        form.instance.user_creator = self.request.user
        context = self.get_context_data()
        attachment_formset = context['attachment_formset']
        if form.is_valid() and attachment_formset.is_valid():
            self.object = form.save()
            attachment_formset.instance = self.object
            attachment_formset.save()
            if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({"message": "Changes saved successfully!"})
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('incidents:detail', args=[self.object.pk])

    
@method_decorator(login_required, name='dispatch')
class IncidentTableView(LoginRequiredMixin, generic.ListView):
    model = Incident
    template_name = "incidents/table.html"
    context_object_name = "incidents"

    def get_queryset(self):
        """Regresar todos los incidentes por fecha más reciente para el usuario autenticado."""
        query = self.request.GET.get("q", "")
        ordering = self.request.GET.get("ordering", "-pub_date")
        user_creator = self.request.GET.get("user_creator")
        
        # Filtra los incidentes basándose en el usuario y el parámetro de búsqueda
        incidents = Incident.objects.filter(
            user_creator=self.request.user,
            incident_text__icontains=query,
        ).order_by(ordering)
        
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

class DeleteAttachmentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        attachment = get_object_or_404(Attachment, pk=pk)
        incident = attachment.incident

        # Ensure the user has permission
        if incident.user_creator != request.user:
            return HttpResponseForbidden("No tienes permiso para eliminar este adjunto.")

        # Delete the file and the database record
        try:
            attachment.file.delete(save=False)
            attachment.delete()
            messages.success(request, "Adjunto eliminado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al eliminar el adjunto: {e}")

        return redirect('incidents:detail', incident.pk)