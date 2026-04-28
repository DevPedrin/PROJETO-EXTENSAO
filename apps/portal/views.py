from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'portal/home.html')

def delegacias(request):
    return render(request, 'portal/delegacias.html')

def denuncia(request):
    return render(request, 'portal/denuncia.html')

def estatisticas(request):
    return render(request, 'portal/estatisticas.html')

def videos(request):
    return render(request, 'portal/videos.html')