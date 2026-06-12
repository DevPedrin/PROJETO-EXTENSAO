from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
    qs = (
        Denuncia.objects
        .filter(autor_hash=gerar_hash_usuario(request.user))
        .order_by('-criado_em')
    )

    try:
        per_page = int(request.GET.get('per_page', 25))
    except (TypeError, ValueError):
        per_page = 25
    per_page = max(5, min(per_page, 200))

    page_number = request.GET.get('page', 1)
    paginator = Paginator(qs, per_page)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(
        request,
        'portal/dashboard_usuario.html',
        {'denuncias': page_obj, 'paginator': paginator}
    )


@login_required
@requer_moderador_ou_admin
def dashboard_moderador(request):
    qs = Denuncia.objects.all().order_by('-criado_em')

    try:
        per_page = int(request.GET.get('per_page', 25))
    except (TypeError, ValueError):
        per_page = 25
    per_page = max(5, min(per_page, 200))

    page_number = request.GET.get('page', 1)
    paginator = Paginator(qs, per_page)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(
        request,
        'portal/dashboard_moderador.html',
        {'denuncias': page_obj, 'paginator': paginator}
    )


@login_required
@requer_admin
def dashboard_admin(request):
    qs = Denuncia.objects.all().order_by('-criado_em')
    videos = Video.objects.all().order_by('-criado_em')

    total_analise = qs.filter(status='analise').count()
    total_aprovadas = qs.filter(status='aprovada').count()
    total_rejeitadas = qs.filter(status='rejeitada').count()

    try:
        per_page = int(request.GET.get('per_page', 25))
    except (TypeError, ValueError):
        per_page = 25
    per_page = max(5, min(per_page, 200))

    page_number = request.GET.get('page', 1)
    paginator = Paginator(qs, per_page)
    try:
        page_obj = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(
        request,
        'portal/dashboard_admin.html',
        {
            'denuncias': page_obj,
            'videos': videos,
            'paginator': paginator,
            'total_analise': total_analise,
            'total_aprovadas': total_aprovadas,
            'total_rejeitadas': total_rejeitadas,
        }
    )