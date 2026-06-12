from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        'portal/minhas_denuncias.html',
        {'denuncias': page_obj, 'paginator': paginator}
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