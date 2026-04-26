from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("home")

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # 🔥 valida se já existe
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Usuário já existe"
            })

        user = User.objects.create_user(
            username=username,
            password=password
        )

        login(request, user)
        return redirect("portal:home")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")