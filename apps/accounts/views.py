from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            return redirect("portal:home")
        else:
            return render(request, "accounts/login.html", {
                "error": "Usuário ou senha inválidos."
            })

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        # 👈 NOVOS CAMPOS CAPTURADOS DO HTML
        nome_completo = request.POST.get("nome_completo")
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")

        # Validações de campos obrigatórios primários
        if not username or not email or not password:
            return render(request, "accounts/register.html", {
                "error": "Username, E-mail e Senha são obrigatórios."
            })

        # Valida se o username já existe
        if User.objects.filter(username=username).exists():
            return render(request, "accounts/register.html", {
                "error": "Este nome de usuário já está em uso."
            })

        # Valida se o e-mail já existe
        if User.objects.filter(email=email).exists():
            return render(request, "accounts/register.html", {
                "error": "Este e-mail já está cadastrado em outra conta."
            })

        # Valida se o CPF já existe (caso tenha sido preenchido)
        if cpf and User.objects.filter(cpf=cpf).exists():
            return render(request, "accounts/register.html", {
                "error": "Este CPF já está cadastrado em outra conta."
            })

        # CRIA O USUÁRIO E ADICIONA OS CAMPOS EXTRAS
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            nome_completo=nome_completo if nome_completo else "",
            telefone=telefone if telefone else "",
            cpf=cpf if cpf else None  # Evita que salve string vazia no campo unique
        )

        login(request, user)
        return redirect("portal:home")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("portal:home")


@login_required
def profile_view(request):
    user = request.user
    error_message = None
    success_message = None

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        nome_completo = request.POST.get("nome_completo")
        telefone = request.POST.get("telefone")
        cpf = request.POST.get("cpf")
        nova_senha = request.POST.get("nova_senha")

        # 1. Validações básicas de campos obrigatórios
        if not username or not email:
            error_message = "Usuário e E-mail são obrigatórios."
        
        # 2. Valida se o username já existe em OUTRO usuário
        elif User.objects.filter(username=username).exclude(id=user.id).exists():
            error_message = "Este nome de usuário já está em uso."

        # 3. Valida se o e-mail já existe em OUTRO usuário
        elif User.objects.filter(email=email).exclude(id=user.id).exists():
            error_message = "Este e-mail já está em uso por outra conta."

        # 4. Valida se o CPF já existe em OUTRO usuário (caso tenha sido digitado)
        elif cpf and User.objects.filter(cpf=cpf).exclude(id=user.id).exists():
            error_message = "Este CPF já está cadastrado em outra conta."

        else:
            # Tudo certo! Atualiza os dados no objeto do usuário logado
            user.username = username
            user.email = email
            user.nome_completo = nome_completo
            user.telefone = telefone
            user.cpf = cpf if cpf else None # Garante que salva nulo se estiver em branco

            # Se o usuário digitou algo no campo de nova senha, atualiza ela também
            if nova_senha and nova_senha.strip() != "":
                user.set_password(nova_senha)
                # Como a senha mudou, precisamos re-autenticar a sessão do usuário
                from django.contrib.auth import update_session_auth_hash
                user.save()
                update_session_auth_hash(request, user)
            else:
                user.save()

            success_message = "Perfil atualizado com sucesso!"

    return render(request, "accounts/profile.html", {
        "error": error_message,
        "success": success_message,
        "user_profile": user # Passamos os dados do usuário para o template preencher os inputs
    })