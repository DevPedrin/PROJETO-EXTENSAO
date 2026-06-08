from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Isso faz o modelo aparecer no painel e permite gerenciar permissões
    list_display = ('username', 'email', 'is_staff', 'is_superuser')
