from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('contas/', include('accounts.urls')),
    path('', include('acervo.urls')),
    path('', include('core.urls')),
]
