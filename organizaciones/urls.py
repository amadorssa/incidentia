from django.urls import path
from .views import create_organization, join_organization, my_organizations, organization_detail, delete_user

urlpatterns = [
    path('create/', create_organization, name='create_organization'),
    path('join/', join_organization, name='join_organization'),
    path('organizations/', my_organizations, name='my_organizations'),
    path('<slug:slug>/', organization_detail, name='organization_detail'),
    path('<slug:slug>/delete/<int:usuario_id>', delete_user, name='delete_user')
]
