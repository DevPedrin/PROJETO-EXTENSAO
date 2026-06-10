from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from ..forms import DenunciaForm
from ..models import Denuncia
from ..utils import gerar_hash_usuario


@login_required
def denuncia_form(request):
    if request.method == 'POST':
        form = DenunciaForm(request.POST)
        if form.is_valid():
            denuncia = form.save(commit=False)
            denuncia.autor_hash = gerar_hash_usuario(request.user)
            if not form.cleaned_data.get('anonima'):
                denuncia.usuario = request.user
            denuncia.save()
            messages.success(
                request,
                f'Denúncia registrada com protocolo {denuncia.protocolo}.'
            )
            return redirect('portal:dashboard_usuario')
    else:
        form = DenunciaForm()
    return render(request, 'portal/denuncia_form.html', {'form': form})


@login_required
def minhas_denuncias(request):
    denuncias = (
        Denuncia.objects
        .filter(autor_hash=gerar_hash_usuario(request.user))
        .order_by('-criado_em')
    )
    return render(
        request,
        'portal/minhas_denuncias.html',
        {'denuncias': denuncias}
    )


@login_required
def detalhe_denuncia(request, pk):
    denuncia = get_object_or_404(
        Denuncia,
        pk=pk,
        autor_hash=gerar_hash_usuario(request.user)
    )
    return render(
        request,
        'portal/detalhe_denuncia.html',
        {'denuncia': denuncia}
    )