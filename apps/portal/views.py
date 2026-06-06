from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import os
from django.http import HttpResponse, Http404

from .forms import DenunciaForm
from apps.accounts.models import User


def home(request):
    return render(request, 'portal/home.html')


def delegacias(request):
    return render(request, 'portal/delegacias.html')


@login_required
def denuncia(request):
    """
    View de denúncias com anonimato garantido no backend.

    Regra de segurança central:
        - O campo `usuario` NUNCA vem do formulário/POST.
        - Se `anonima=True`, o usuário real é DESCARTADO e substituído
          pelo usuário técnico fixo `anonimo_sistema`.
        - Isso impede qualquer tentativa de manipulação via API ou frontend.
    """
    if request.method == 'POST':
        form = DenunciaForm(request.POST)

        if form.is_valid():
            # Não salva ainda — precisamos definir `usuario` antes
            nova_denuncia = form.save(commit=False)
            anonima = form.cleaned_data.get('anonima', False)

            if anonima:
                # ── Modo anônimo ────────────────────────────────────────────
                # Ignora COMPLETAMENTE o usuário autenticado.
                # Usa o usuário técnico fixo definido nas settings.
                # Nenhum log, nenhuma FK, nenhum vínculo com request.user.
                try:
                    usuario_anonimo = User.objects.get(
                        username=settings.ANONYMOUS_COMPLAINT_USERNAME
                    )
                except User.DoesNotExist:
                    # Falha segura + Self-healing: se o usuário técnico não existir
                    # (ex: migration não rodou ou foi apagado), recria ele automaticamente.
                    usuario_anonimo = User.objects.create(
                        username=settings.ANONYMOUS_COMPLAINT_USERNAME,
                        email='anonimo@sistema.local',
                        first_name='Usuário',
                        last_name='Anônimo',
                        is_active=False,
                        is_staff=False,
                        is_superuser=False,
                    )
                    usuario_anonimo.set_unusable_password()
                    usuario_anonimo.save()

                nova_denuncia.usuario = usuario_anonimo

            else:
                # ── Modo identificado ────────────────────────────────────────
                # Usa o usuário autenticado da sessão atual.
                nova_denuncia.usuario = request.user

            nova_denuncia.save()

            messages.success(
                request,
                '✅ Denúncia registrada com sucesso! Obrigado pela sua contribuição.'
            )
            return redirect('portal:denuncia')

        # Formulário inválido — reexibe com erros
        return render(request, 'portal/denuncia.html', {'form': form})

    # GET — exibe formulário vazio
    form = DenunciaForm()
    return render(request, 'portal/denuncia.html', {'form': form})


def estatisticas(request):
    return render(request, 'portal/estatisticas.html')


def videos(request):
    return render(request, 'portal/videos.html')


def documentacao(request):
    if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
        raise Http404("Documentação técnica não encontrada.")
    path = os.path.join(settings.BASE_DIR, 'documentação', 'index.html')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html; charset=utf-8')
    raise Http404("Documentação técnica não encontrada.")


@login_required
def minhas_denuncias(request):
    """
    Exibe apenas as denúncias vinculadas ao usuário logado.
    Denúncias anônimas não aparecerão aqui por estarem vinculadas
    ao usuário técnico 'anonimo_sistema', preservando o sigilo.
    """
    from .models import Denuncia
    denuncias = Denuncia.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'portal/minhas_denuncias.html', {'denuncias': denuncias})


@login_required
def todas_denuncias(request):
    """
    Exibe TODAS as denúncias cadastradas (painel geral).
    Acesso restrito apenas a administradores/equipe.
    """
    if not (request.user.is_staff or request.user.is_superuser):
        raise Http404("Página não encontrada.")
        
    from .models import Denuncia
    denuncias = Denuncia.objects.all().order_by('-criado_em')
    return render(request, 'portal/todas_denuncias.html', {'denuncias': denuncias})