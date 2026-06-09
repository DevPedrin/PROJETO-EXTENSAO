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
    """Gera estatísticas baseadas nos tipos de golpes das denúncias aprovadas."""
    # Filtro corrigido para 'aprovada' (minúsculo) conforme definido no Choice do Model
    total_denuncias = Denuncia.objects.filter(status='aprovada').count()
    
    # Agrupa e conta o número de denúncias por tipo de golpe cadastrado
    denuncias_por_tipo = (
        Denuncia.objects.filter(status='aprovada')
        .values('tipo_golpe')
        .annotate(total=models.Count('id'))
        .order_by('-total')
    )
    
    # Mapeamento para exibir os labels amigáveis do Choice no template
    escolhas_golpe = dict(Denuncia.TIPOS_GOLPE)
    
    # Adiciona a porcentagem e o nome amigável a cada item do agrupamento
    for item in denuncias_por_tipo:
        item['nome_golpe'] = escolhas_golpe.get(item['tipo_golpe'], item['tipo_golpe'])
        if total_denuncias > 0:
            item['porcentagem'] = round((item['total'] / total_denuncias) * 100)
        else:
            item['porcentagem'] = 0

    # Golpe mais comum
    golpe_mais_comum = "Nenhum registrado"
    if denuncias_por_tipo:
        golpe_mais_comum = denuncias_por_tipo[0]['nome_golpe']

    # Total de cidades atendidas/afetadas pelas denúncias aprovadas
    total_cidades = Denuncia.objects.filter(status='aprovada').exclude(cidade='').values('cidade').distinct().count()

    context = {
        'total_denuncias': total_denuncias,
        'denuncias_por_tipo': denuncias_por_tipo,
        'golpe_mais_comum': golpe_mais_comum,
        'total_cidades': total_cidades,
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