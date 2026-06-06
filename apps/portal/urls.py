from django.contrib import admin
from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('delegacias/', views.delegacias, name='delegacias'),
    path('denuncia/', views.denuncia, name='denuncia'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('videos/', views.videos, name='videos'),
    path('documentacao/', views.documentacao, name='documentacao'),
    path('documentação/', views.documentacao, name='documentacao_alt'),
    path('minhas-denuncias/', views.minhas_denuncias, name='minhas_denuncias'),
    path('todas-denuncias/', views.todas_denuncias, name='todas_denuncias'),
    path('admin/', admin.site.urls),
]