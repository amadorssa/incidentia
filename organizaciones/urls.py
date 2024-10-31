from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crear_organizacion, name='crear_organizacion'),
    path('unirse/', views.unirse_organizacion, name='unirse_organizacion'),
    path('mis-organizaciones/', views.mis_organizaciones, name='mis_organizaciones'),
    path('organizacion/<int:organizacion_id>/', views.ver_organizacion, name='ver_organizacion'),
]
