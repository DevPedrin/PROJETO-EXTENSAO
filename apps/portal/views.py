from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import Delegacia, VideoEducativo, Denuncia, AnexoDenuncia

def home(request):
    return render(request, 'portal/home.html')

def delegacias(request):
    todas_delegacias = Delegacia.objects.all()
    return render(request, 'portal/delegacias.html', {'delegacias': todas_delegacias})

@login_required
def denuncia(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        delegacia_id = request.POST.get('delegacia')
        anonimo = request.POST.get('anonimo') == 'on'
        
        delegacia = None
        if delegacia_id:
            delegacia = Delegacia.objects.get(id=delegacia_id)
            
        denuncia = Denuncia.objects.create(
            titulo=titulo,
            descricao=descricao,
            delegacia=delegacia,
            anonimo=anonimo,
            autor=request.user
        )
        
        # Lógica de anexos (simplificada)
        arquivos = request.FILES.getlist('arquivos')
        for f in arquivos:
            AnexoDenuncia.objects.create(denuncia=denuncia, arquivo=f)
            
        return render(request, 'portal/denuncia.html', {'sucesso': True})

    delegacias = Delegacia.objects.all()
    return render(request, 'portal/denuncia.html', {'delegacias': delegacias})

def estatisticas(request):
    # Estatísticas reais baseadas em denúncias aprovadas
    total_denuncias = Denuncia.objects.filter(status='APROVADA').count()
    denuncias_por_delegacia = Delegacia.objects.filter(denuncias__status='APROVADA').annotate(total=models.Count('denuncias')).order_by('-total')
    
    # Adiciona porcentagem a cada delegacia para o gráfico
    for del_item in denuncias_por_delegacia:
        if total_denuncias > 0:
            del_item.porcentagem = (del_item.total / total_denuncias) * 100
        else:
            del_item.porcentagem = 0

    context = {
        'total_denuncias': total_denuncias,
        'denuncias_por_delegacia': denuncias_por_delegacia,
    }
    return render(request, 'portal/estatisticas.html', context)

def videos(request):
    todos_videos = VideoEducativo.objects.all()
    return render(request, 'portal/videos.html', {'videos': todos_videos})
