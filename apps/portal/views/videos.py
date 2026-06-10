from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..models import Video
from ..permissions import requer_moderador_ou_admin


@login_required
@requer_moderador_ou_admin
def cadastrar_video(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        url = request.POST.get('url_youtube')

        if titulo and url:
            Video.objects.create(
                titulo=titulo,
                descricao=descricao,
                url_youtube=url
            )
            messages.success(request, 'Vídeo cadastrado com sucesso!')
            return redirect('portal:dashboard')

    return render(request, 'portal/cadastrar_video.html')