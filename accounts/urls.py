from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('entrar/', views.EntrarView.as_view(), name='login'),
    # LogoutView do Django só aceita POST (protegido por CSRF).
    path('sair/', LogoutView.as_view(), name='logout'),
    path('cadastro/', views.cadastro, name='cadastro'),
]
