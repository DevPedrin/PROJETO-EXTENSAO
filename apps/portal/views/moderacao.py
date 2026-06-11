from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils import timezone

from ..models import Denuncia
from ..permissions import requer_moderador, requer_moderador_ou_admin


@login_required
@requer_moderador
def moderacao_denuncias(request):
    denuncias = Denuncia.objects.all()
    return render(
        request,
        'portal/moderacao_denuncias.html',
        {'denuncias': denuncias}
    )


@login_required
@requer_moderador
def alterar_status_denuncia(request, pk, acao):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if acao == 'aprovar':
        denuncia.status = 'aprovada'
        denuncia.moderado_por = request.user
        denuncia.moderado_em = timezone.now()
        denuncia.save()
        messages.success(request, f'{denuncia.protocolo} aprovada.')

    elif acao == 'rejeitar':
        denuncia.status = 'rejeitada'
        denuncia.moderado_por = request.user
        denuncia.moderado_em = timezone.now()
        denuncia.save()
        messages.warning(request, f'{denuncia.protocolo} rejeitada.')

    elif acao == 'apagar':
        if not request.user.tipo_usuario == 'admin':
            raise Http404()
        denuncia.delete()
        messages.error(request, f'Denúncia removida.')

    return redirect('portal:dashboard')


@login_required
@requer_moderador
def aprovar_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)
    denuncia.status = 'aprovada'
    denuncia.moderado_por = request.user
    denuncia.moderado_em = timezone.now()
    denuncia.save()
    messages.success(request, f'{denuncia.protocolo} aprovada.')
    return redirect('portal:dashboard')


@login_required
@requer_moderador
def rejeitar_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if request.method == 'POST':
        motivo = request.POST.get('motivo_moderacao')
        denuncia.status = 'rejeitada'
        denuncia.motivo_moderacao = motivo
        denuncia.moderado_por = request.user
        denuncia.moderado_em = timezone.now()
        denuncia.save()
        messages.success(request, f'{denuncia.protocolo} rejeitada.')
        return redirect('portal:dashboard')

    return render(
        request,
        'portal/rejeitar_denuncia.html',
        {'denuncia': denuncia}
    )


@login_required
@requer_moderador_ou_admin
def publicar_denuncia(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)

    if denuncia.status != 'aprovada':
        messages.error(request, 'Somente denúncias aprovadas podem ser publicadas.')
        return redirect('portal:dashboard')

    denuncia.publicada = True
    denuncia.publicada_em = timezone.now()
    denuncia.save()
    messages.success(request, f'{denuncia.protocolo} publicada.')
    return redirect('portal:dashboard')


@login_required
@requer_moderador_ou_admin
def detalhe_denuncia_moderacao(request, pk):
    denuncia = get_object_or_404(Denuncia, pk=pk)
    return render(
        request,
        'portal/detalhe_denuncia_moderacao.html',
        {'denuncia': denuncia}
    )