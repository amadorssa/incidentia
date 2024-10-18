from django.urls import path
from .views import registro, iniciar_sesion

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('iniciar-sesion/', iniciar_sesion, name='iniciar_sesion'),
]
