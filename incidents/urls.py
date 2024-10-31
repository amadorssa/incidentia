from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import IndexView, DetailView, EditIncidentView

app_name = "incidents"
urlpatterns = [
    path('organizacion/<int:organizacion_id>/', IndexView.as_view(), name='index'),  # Modifica para incluir el ID de la organización
    path('incident/<int:pk>/', DetailView.as_view(), name='detail'),
    path('incident/<int:pk>/edit/', EditIncidentView.as_view(), name='edit_incident'),
    path('<int:organizacion_id>/table/', views.IncidentTableView.as_view(), name='incident_table'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
