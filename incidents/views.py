from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic

from .forms import IncidentForm
from .models import Choice, Incident


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


class ResultsView(generic.DetailView):
    model = Incident
    template_name = "incidents/results.html"


def vote(request, incident_id):
    incident = get_object_or_404(Incident, pk=incident_id)
    try:
        selected_choice = incident.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "incidents/detail.html",
            {
                "incident": incident,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("incidents:results", args=(incident.id,)))