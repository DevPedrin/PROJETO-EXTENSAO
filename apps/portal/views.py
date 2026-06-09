from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, Http404
from django.db import models
import os

from .forms import DenunciaForm
from .models import Denuncia, Video
from apps.accounts.models import User

# ─── Funções Auxiliares de Permissão ──────────────────────────────────────────
def eh_moderador_ou_admin(user):
    return user.is_authenticated and user.tipo_usuario in ['moderador', 'admin']

def eh_admin(user):
    return user.is_authenticated and user.tipo_usuario == 'admin'


# ─── Rotas Públicas Base ──────────────────────────────────────────────────────
def home(request):
    return render(request, 'portal/home.html')


def delegacias(request):
    from .models import Delegacia
    lista = Delegacia.objects.filter(ativo=True)
    context = {
        'delegacias': lista,
        'cidades': lista.exclude(cidade='').values_list('cidade', flat=True).distinct().order_by('cidade'),
        'tipos': Delegacia.TIPOS,
    }
    return render(request, 'portal/delegacias.html', context)


def estatisticas(request):
    """Estatísticas enriquecidas das denúncias aprovadas."""
    from django.db.models.functions import TruncMonth
    import json

    aprovadas = Denuncia.objects.filter(status='aprovada')
    total_denuncias = aprovadas.count()
    total_em_analise = Denuncia.objects.filter(status='analise').count()
    total_rejeitadas = Denuncia.objects.filter(status='rejeitada').count()

    escolhas_golpe = dict(Denuncia.TIPOS_GOLPE)
    escolhas_faixa = dict(Denuncia.FAIXAS_ETARIAS)

    # Por tipo de golpe
    denuncias_por_tipo = list(
        aprovadas.values('tipo_golpe')
        .annotate(total=models.Count('id'))
        .order_by('-total')
    )
    for item in denuncias_por_tipo:
        item['nome_golpe'] = escolhas_golpe.get(item['tipo_golpe'], item['tipo_golpe'])
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

    # Por faixa etária
    denuncias_por_faixa = list(
        aprovadas.exclude(faixa_etaria='')
        .values('faixa_etaria')
        .annotate(total=models.Count('id'))
        .order_by('faixa_etaria')
    )
    for item in denuncias_por_faixa:
        item['nome_faixa'] = escolhas_faixa.get(item['faixa_etaria'], item['faixa_etaria'])
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

    # Por cidade (top 5)
    denuncias_por_cidade = list(
        aprovadas.exclude(cidade='')
        .values('cidade')
        .annotate(total=models.Count('id'))
        .order_by('-total')[:5]
    )
    for item in denuncias_por_cidade:
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

    # Evolução mensal (últimos 6 meses)
    from datetime import date
    from dateutil.relativedelta import relativedelta
    hoje = date.today()
    seis_meses_atras = hoje - relativedelta(months=5)

    mensal_qs = (
        Denuncia.objects
        .filter(criado_em__date__gte=seis_meses_atras)
        .annotate(mes=TruncMonth('criado_em'))
        .values('mes')
        .annotate(total=models.Count('id'))
        .order_by('mes')
    )
    meses_labels = [item['mes'].strftime('%b/%Y') for item in mensal_qs]
    meses_valores = [item['total'] for item in mensal_qs]

    context = {
        'total_denuncias': total_denuncias,
        'total_em_analise': total_em_analise,
        'total_rejeitadas': total_rejeitadas,
        'denuncias_por_tipo': denuncias_por_tipo,
        'denuncias_por_faixa': denuncias_por_faixa,
        'denuncias_por_cidade': denuncias_por_cidade,
        'meses_labels_json': json.dumps(meses_labels),
        'meses_valores_json': json.dumps(meses_valores),
    }
    return render(request, 'portal/estatisticas.html', context)


def videos(request):
    # Lista dinamicamente os vídeos cadastrados no banco
    lista_videos = Video.objects.all().order_by('-criado_em')
    return render(request, 'portal/videos.html', {'videos': lista_videos})


# ─── Sistema de Fluxo de Denúncias (Segurança Preservada) ─────────────────────
@login_required
def denuncia(request):
    """View de denúncias com anonimato garantido no backend."""
    if request.method == 'POST':
        form = DenunciaForm(request.POST)

        if form.is_valid():
            nova_denuncia = form.save(commit=False)
            anonima = form.cleaned_data.get('anonima', False)

            if anonima:
                try:
                    usuario_anonimo = User.objects.get(
                        username=settings.ANONYMOUS_COMPLAINT_USERNAME
                    )
                except User.DoesNotExist:
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
                nova_denuncia.usuario = request.user

            nova_denuncia.save()

            messages.success(
                request,
                '✅ Denúncia registrada com sucesso! Obrigado pela sua contribuição.'
            )
            return redirect('portal:denuncia')

        return render(request, 'portal/denuncia.html', {'form': form})

    form = DenunciaForm()
    return render(request, 'portal/denuncia.html', {'form': form})


# ─── Roteador Dinâmico e Painéis (Dashboards) ─────────────────────────────────
@login_required
def dashboard_router(request):
    """Redireciona centralizadamente o usuário com base em seu privilégio."""
    if request.user.tipo_usuario == 'admin':
        return redirect('portal:dashboard_admin')
    elif request.user.tipo_usuario == 'moderador':
        return redirect('portal:dashboard_moderador')
    return redirect('portal:dashboard_usuario')


@login_required
def dashboard_usuario(request):
    """Painel do Usuário Comum: Retorna apenas os registros identificados dele."""
    denuncias = Denuncia.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'portal/dashboard_usuario.html', {'denuncias': denuncias})


@login_required
@user_passes_test(eh_moderador_ou_admin)
def dashboard_moderador(request):
    """Painel de Moderação: Focado em validar denúncias pendentes."""
    denuncias_pendentes = Denuncia.objects.filter(status='analise').order_by('-criado_em')
    return render(request, 'portal/dashboard_moderador.html', {'denuncias': denuncias_pendentes})


@login_required
@user_passes_test(eh_admin)
def dashboard_admin(request):
    """Painel de Administração Global."""
    todas_denuncias = Denuncia.objects.all().order_by('-criado_em')
    todos_videos = Video.objects.all().order_by('-criado_em')
    context = {
        'denuncias': todas_denuncias,
        'videos': todos_videos,
        'total_analise': todas_denuncias.filter(status='analise').count(),
        'total_aprovadas': todas_denuncias.filter(status='aprovada').count(),
    }
    return render(request, 'portal/dashboard_admin.html', context)


# ─── Sistema de Gerenciamento de Denúncias ───────────────────────────────────
@login_required
@user_passes_test(eh_moderador_ou_admin)
def alterar_status_denuncia(request, pk, acao):
    """Permite aprovar, rejeitar ou excluir definitivamente denúncias."""
    denuncia_obj = get_object_or_404(Denuncia, pk=pk)
    
    if acao == 'aprovar':
        denuncia_obj.status = 'aprovada'
        denuncia_obj.save()
        messages.success(request, f"Denúncia #{pk} aprovada com sucesso.")
    elif acao == 'rejeitar':
        denuncia_obj.status = 'rejeitada'
        denuncia_obj.save()
        messages.warning(request, f"Denúncia #{pk} marcada como rejeitada.")
    elif acao == 'apagar':
        if request.user.tipo_usuario == 'admin':
            denuncia_obj.delete()
            messages.error(request, f"Denúncia #{pk} excluída permanentemente.")
        else:
            raise Http404("Apenas administradores podem deletar dados.")
            
    return redirect('portal:dashboard')


# ─── Sistema de Cadastro de Vídeos ──────────────────────────────────────────
@login_required
@user_passes_test(eh_moderador_ou_admin)
def cadastrar_video(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        url = request.POST.get('url_youtube')
        
        if titulo and url:
            Video.objects.create(titulo=titulo, descricao=descricao, url_youtube=url)
            messages.success(request, 'Vídeo cadastrado com sucesso!')
            return redirect('portal:dashboard')
            
    return render(request, 'portal/cadastrar_video.html')


# ─── Outras Funções Legadas mantidas por segurança ───────────────────────────
def documentacao(request):
    if not request.user.is_authenticated or (not request.user.is_staff and not request.user.is_superuser):
        raise Http404("Documentação técnica não encontrada.")
    path_doc = os.path.join(settings.BASE_DIR, 'documentação', 'index.html')
    if os.path.exists(path_doc):
        with open(path_doc, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html; charset=utf-8')
    raise Http404("Documentação técnica não encontrada.")


@login_required
def minhas_denuncias(request):
    return redirect('portal:dashboard_usuario')


@login_required
def todas_denuncias(request):
    if not (request.user.is_staff or request.user.is_superuser or request.user.tipo_usuario in ['admin', 'moderador']):
        raise Http404("Página não encontrada.")
    return redirect('portal:dashboard')

# ─── Painel de Gerenciamento de Delegacias (Admin) ───────────────────────────
@login_required
@user_passes_test(eh_admin)
def painel_delegacias(request):
    from .models import Delegacia
    from .forms import DelegaciaForm

    if request.method == 'POST':
        pk = request.POST.get('pk')
        acao = request.POST.get('acao')

        if acao == 'excluir' and pk:
            Delegacia.objects.filter(pk=pk).delete()
            messages.success(request, 'Delegacia removida com sucesso.')
            return redirect('portal:painel_delegacias')

        if acao == 'toggle_ativo' and pk:
            d = get_object_or_404(Delegacia, pk=pk)
            d.ativo = not d.ativo
            d.save()
            messages.success(request, f'Delegacia {"ativada" if d.ativo else "desativada"}.')
            return redirect('portal:painel_delegacias')

        pk_editar = request.POST.get('pk_editar')
        if pk_editar:
            instancia = get_object_or_404(Delegacia, pk=pk_editar)
            form = DelegaciaForm(request.POST, instance=instancia)
            if form.is_valid():
                form.save()
                messages.success(request, 'Delegacia atualizada com sucesso.')
                return redirect('portal:painel_delegacias')
        else:
            form = DelegaciaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Delegacia cadastrada com sucesso.')
                return redirect('portal:painel_delegacias')
    else:
        form = DelegaciaForm()

    delegacias = Delegacia.objects.all()
    return render(request, 'portal/painel_delegacias.html', {
        'form': form,
        'delegacias': delegacias,
    })