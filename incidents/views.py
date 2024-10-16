from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .forms import IncidentForm
from .models import Incident

class IndexView(generic.ListView):
    template_name = "incidents/index.html"
    context_object_name = "latest_incident_list"

    def get_queryset(self):
        """Return the last five published incidents."""
        return Incident.objects.order_by("-pub_date")[:5]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = IncidentForm()  # Añadir el formulario al contexto
        return context

    def post(self, request, *args, **kwargs):
        form = IncidentForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el nuevo incidente
            return redirect("incidents:index")  # Redirecciona al index
        return self.get(request, *args, **kwargs)  # Si no es válido, muestra el formulario

class DetailView(generic.DetailView):
    model = Incident
    template_name = "incidents/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = IncidentForm(instance=self.object)  # Añadir el formulario con la instancia actual
        return context

    def post(self, request, *args, **kwargs):
        incident = self.get_object()
        form = IncidentForm(request.POST, instance=incident)  # Asociar el formulario con el incidente
        if form.is_valid():
            form.save()  # Guardar los cambios
            return redirect('incidents:detail', pk=incident.pk)  # Redireccionar a la vista de detalle
        return self.render_to_response({'form': form})  # Renderizar de nuevo si no es válido
