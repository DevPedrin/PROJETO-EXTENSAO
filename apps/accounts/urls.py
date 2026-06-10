from django.urls import path
from .views import (
    login_view,
    register_view,
    logout_view,
    profile_view,
    usuarios_view,
    editar_usuario_view,
    excluir_usuario_view,
    criar_usuario_view
)

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),

    path('usuarios/', usuarios_view, name='usuarios'),
    path('usuarios/novo/', criar_usuario_view, name='usuario_criar'),
    path('usuarios/<int:user_id>/editar/', editar_usuario_view, name='usuario_editar'),
    path('usuarios/<int:user_id>/excluir/', excluir_usuario_view, name='usuario_excluir'),
]