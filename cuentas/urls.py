from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import registro, iniciar_sesion, perfil, cerrar_sesion

urlpatterns = [
    path('registro/', registro, name='registro'),
    path('iniciar-sesion/', iniciar_sesion, name='iniciar_sesion'),
    path('perfil/', perfil, name='perfil'),
    path('cerrar-sesion/', cerrar_sesion, name='cerrar_sesion'),  # Nueva URL para cerrar sesión
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)