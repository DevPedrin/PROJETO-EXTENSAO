from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('delegacias/', views.delegacias, name='delegacias'),
    path('denuncia/', views.denuncia, name='denuncia'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('golpes/', views.golpes, name='golpes'),
    path('videos/', views.videos, name='videos'),
]