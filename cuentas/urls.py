from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import sign_up, sign_in, profile, sign_out, edit_profile, change_pass

app_name = "accounts"
urlpatterns = [
    path('signup/', sign_up, name='sign_up'),
    path('login/', sign_in, name='sign_in'),
    path('<slug:slug>/profile/', profile, name='profile'),
    path('logout/', sign_out, name='sign_out'),
    path('<slug:slug>/edit_profile/', edit_profile, name='edit_profile'),
    path('<slug:slug>/change_pass/', change_pass, name='change_pass')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)