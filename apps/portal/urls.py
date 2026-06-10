from django.urls import path

from .views.publicas import home, delegacias, videos, denuncias_publicadas
from .views.dashboards import (
    dashboard_router, dashboard_usuario,
    dashboard_moderador, dashboard_admin,
)
from .views.denuncias import (
    denuncia_form,
    minhas_denuncias,
    detalhe_denuncia,
)
from .views.moderacao import (
    alterar_status_denuncia, moderacao_denuncias,
    aprovar_denuncia, rejeitar_denuncia, publicar_denuncia,
    detalhe_denuncia_moderacao,
)
from .views.moderacao import (
    alterar_status_denuncia, moderacao_denuncias,
    aprovar_denuncia, rejeitar_denuncia, publicar_denuncia,
)
from .views.delegacias import painel_delegacias
from .views.videos import cadastrar_video
from .views.sistema import estatisticas, documentacao

app_name = 'portal'

urlpatterns = [
    # Públicas
    path('', home, name='home'),
    path('videos/', videos, name='videos'),
    path('delegacias/', delegacias, name='delegacias'),
    path('estatisticas/', estatisticas, name='estatisticas'),
    path('denuncias-publicadas/', denuncias_publicadas, name='denuncias_publicadas'),
    path('documentacao/', documentacao, name='documentacao'),

    # Denúncias
    path('denuncia/', denuncia_form, name='denuncia'),
    path('minhas-denuncias/', minhas_denuncias, name='minhas_denuncias'),
    path('minhas-denuncias/<int:pk>/', detalhe_denuncia, name='detalhe_denuncia'),

    # Moderação
    path('moderacao/detalhe/<int:pk>/', detalhe_denuncia_moderacao, name='detalhe_denuncia_moderacao'),
    path('moderacao/', moderacao_denuncias, name='moderacao_denuncias'),
    path('moderacao/aprovar/<int:pk>/', aprovar_denuncia, name='aprovar_denuncia'),
    path('moderacao/rejeitar/<int:pk>/', rejeitar_denuncia, name='rejeitar_denuncia'),
    path('moderacao/publicar/<int:pk>/', publicar_denuncia, name='publicar_denuncia'),
    path('moderacao/<int:pk>/<str:acao>/', alterar_status_denuncia, name='alterar_status_denuncia'),

    # Admin
    path('videos/cadastrar/', cadastrar_video, name='cadastrar_video'),
    path('painel/delegacias/', painel_delegacias, name='painel_delegacias'),

    # Dashboards
    path('dashboard/', dashboard_router, name='dashboard'),
    path('dashboard/usuario/', dashboard_usuario, name='dashboard_usuario'),
    path('dashboard/moderador/', dashboard_moderador, name='dashboard_moderador'),
    path('dashboard/admin/', dashboard_admin, name='dashboard_admin'),
]