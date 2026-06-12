from django.shortcuts import render
from django.db import models
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Denuncia, Video, Delegacia


def home(request):
    return render(
        request,
        'portal/home.html'
    )


def delegacias(request):

    lista = Delegacia.objects.filter(
        ativo=True
    )

    context = {
        'delegacias': lista,
        'cidades': (
            lista.exclude(cidade='')
            .values_list(
                'cidade',
                flat=True
            )
            .distinct()
            .order_by('cidade')
        ),
        'tipos': Delegacia.TIPOS,
    }

    return render(
        request,
        'portal/delegacias.html',
        context
    )


def videos(request):

    lista_videos = (
        Video.objects
        .all()
        .order_by('-criado_em')
    )

    return render(
        request,
        'portal/videos.html',
        {
            'videos': lista_videos
        }
    )


def denuncias_publicadas(request):
    qs = (
        Denuncia.objects
        .filter(publicada=True)
        .order_by('-publicada_em')
    )

    # Paginação para evitar carregar todas as denúncias na memória
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
        'portal/denuncias_publicadas.html',
        {
            'denuncias': page_obj,
            'paginator': paginator,
        }
    )