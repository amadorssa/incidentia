from django.urls import path
from . import views

app_name = "incidents"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/edit/", views.EditIncidentView.as_view(), name="edit"),
]
