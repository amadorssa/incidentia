from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = "incidents"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditIncidentView.as_view(), name="edit"),
    path("table/", views.IncidentTableView.as_view(), name="incident_table"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
