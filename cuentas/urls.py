from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import sign_up, sign_in, profile, sign_out, edit_profile

urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('login/', sign_in, name='sign_in'),
    path('profile/', profile, name='profile'),
    path('logout/', sign_out, name='sign_out'),
    path('edit_profile/', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)