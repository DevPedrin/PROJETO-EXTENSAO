# apps/portal/views/__init__.py

from .publicas import (
    home,
    delegacias,
    videos,
    denuncias_publicadas,
)
from .dashboards import (
    dashboard_router,
    dashboard_usuario,
    dashboard_moderador,
    dashboard_admin,
)
from .denuncias import (
    denuncia_form,
    minhas_denuncias,
    detalhe_denuncia,
)
from .moderacao import (
    alterar_status_denuncia,
    moderacao_denuncias,
    aprovar_denuncia,
    rejeitar_denuncia,
    publicar_denuncia,
)
from .delegacias import painel_delegacias
from .videos import cadastrar_video
from .sistema import (
    estatisticas,
    documentacao,
)