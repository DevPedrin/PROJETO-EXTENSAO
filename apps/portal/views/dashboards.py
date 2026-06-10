from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Denuncia, Video
from ..permissions import requer_admin, requer_moderador_ou_admin
from ..utils import gerar_hash_usuario


@login_required
def dashboard_router(request):
    if request.user.tipo_usuario == 'admin':
        return redirect('portal:dashboard_admin')
    if request.user.tipo_usuario == 'moderador':
        return redirect('portal:dashboard_moderador')
    return redirect('portal:dashboard_usuario')


@login_required
def dashboard_usuario(request):
    denuncias = (
        Denuncia.objects
        .filter(autor_hash=gerar_hash_usuario(request.user))
        .order_by('-criado_em')
    )
    return render(
        request,
        'portal/dashboard_usuario.html',
        {'denuncias': denuncias}
    )


@login_required
@requer_moderador_ou_admin
def dashboard_moderador(request):
    denuncias = Denuncia.objects.all().order_by('-criado_em')
    return render(
        request,
        'portal/dashboard_moderador.html',
        {'denuncias': denuncias}
    )


@login_required
@requer_admin
def dashboard_admin(request):
    denuncias = Denuncia.objects.all().order_by('-criado_em')
    videos = Video.objects.all().order_by('-criado_em')
    return render(
        request,
        'portal/dashboard_admin.html',
        {
            'denuncias': denuncias,
            'videos': videos,
            'total_analise': denuncias.filter(status='analise').count(),
            'total_aprovadas': denuncias.filter(status='aprovada').count(),
            'total_rejeitadas': denuncias.filter(status='rejeitada').count(),
        }
    )