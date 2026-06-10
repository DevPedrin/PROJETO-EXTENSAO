from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import models
from django.conf import settings
import os

from ..models import Denuncia


def estatisticas(request):
    from django.db.models.functions import TruncMonth
    from datetime import date
    from dateutil.relativedelta import relativedelta
    import json

    aprovadas = Denuncia.objects.filter(status='aprovada')
    total_denuncias = aprovadas.count()
    total_em_analise = Denuncia.objects.filter(status='analise').count()
    total_rejeitadas = Denuncia.objects.filter(status='rejeitada').count()

    escolhas_golpe = dict(Denuncia.TIPOS_GOLPE)
    escolhas_faixa = dict(Denuncia.FAIXAS_ETARIAS)

    denuncias_por_tipo = list(
        aprovadas.values('tipo_golpe')
        .annotate(total=models.Count('id'))
        .order_by('-total')
    )
    for item in denuncias_por_tipo:
        item['nome_golpe'] = escolhas_golpe.get(item['tipo_golpe'], item['tipo_golpe'])
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

    denuncias_por_faixa = list(
        aprovadas.exclude(faixa_etaria='')
        .values('faixa_etaria')
        .annotate(total=models.Count('id'))
        .order_by('faixa_etaria')
    )
    for item in denuncias_por_faixa:
        item['nome_faixa'] = escolhas_faixa.get(item['faixa_etaria'], item['faixa_etaria'])
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

    denuncias_por_cidade = list(
        aprovadas.exclude(cidade='')
        .values('cidade')
        .annotate(total=models.Count('id'))
        .order_by('-total')[:5]
    )
    for item in denuncias_por_cidade:
        item['porcentagem'] = round((item['total'] / total_denuncias) * 100, 1) if total_denuncias else 0

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


def documentacao(request):
    if not request.user.is_authenticated or (
        not request.user.is_staff and not request.user.is_superuser
    ):
        raise Http404("Documentação técnica não encontrada.")
    path_doc = os.path.join(settings.BASE_DIR, 'documentação', 'index.html')
    if os.path.exists(path_doc):
        with open(path_doc, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type='text/html; charset=utf-8')
    raise Http404("Documentação técnica não encontrada.")