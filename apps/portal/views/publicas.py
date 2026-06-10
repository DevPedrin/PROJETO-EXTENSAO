from django.shortcuts import render
from django.db import models

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

    denuncias = (
        Denuncia.objects
        .filter(publicada=True)
        .order_by('-publicada_em')
    )

    return render(
        request,
        'portal/denuncias_publicadas.html',
        {
            'denuncias': denuncias
        }
    )