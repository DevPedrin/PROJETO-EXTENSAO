from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    # Páginas Institucionais Públicas
    path('', views.home, name='home'),
    path('delegacias/', views.delegacias, name='delegacias'),
    path('estatisticas/', views.estatisticas, name='estatisticas'),
    path('videos/', views.videos, name='videos'),
    
    # Sistema de Ocorrências
    path('denuncia/', views.denuncia, name='denuncia'),
    
    # Núcleo de Dashboards Dinâmicas
    path('dashboard/', views.dashboard_router, name='dashboard'),
    path('dashboard/usuario/', views.dashboard_usuario, name='dashboard_usuario'),
    path('dashboard/moderador/', views.dashboard_moderador, name='dashboard_moderador'),
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    
    # Operações de Controle (Moderação/Gerenciamento)
    path('denuncia/status/<int:pk>/<str:acao>/', views.alterar_status_denuncia, name='alterar_status_denuncia'),
    path('videos/cadastrar/', views.cadastrar_video, name='cadastrar_video'),
    
    # Documentação e Administração Core
    path('documentacao/', views.documentacao, name='documentacao'),
    path('documentação/', views.documentacao, name='documentacao_alt'),
    path('minhas-denuncias/', views.minhas_denuncias, name='minhas_denuncias'),
    path('todas-denuncias/', views.todas_denuncias, name='todas_denuncias'),
    path('admin/', admin.site.urls),
]