from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import AddIncident, DetailView, EditIncidentView

app_name = "incidents"
urlpatterns = [
    # Muestra la vista de índice de incidentes de una organización específica
    path('<slug:slug>/incident/add/', AddIncident.as_view(), name='add_incident'),  # Modifica para incluir el ID de la organización
    
    # Muestra el detalle de un incidente específico
    path('<slug:slug>/incident/<int:pk>/detail/', DetailView.as_view(), name='detail'),
    
    # Permite la edición de un incidente específico
    path('<slug:slug>/incident/<int:pk>/edit/', EditIncidentView.as_view(), name='edit_incident'),

    # Muestra una tabla con los incidentes de una organización específica
    path('<slug:slug>/incident/list/', views.IncidentTableView.as_view(), name='incident_table'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
