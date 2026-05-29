from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
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
    # Mock de estatísticas por enquanto
    total_denuncias = Denuncia.objects.count()
    context = {
        'total_denuncias': total_denuncias,
    }
    return render(request, 'portal/estatisticas.html', context)

def videos(request):
    todos_videos = VideoEducativo.objects.all()
    return render(request, 'portal/videos.html', {'videos': todos_videos})
