from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    STATUS_CHOICES = [
        ('admin', 'Administrador'),
        ('moderador', 'Moderador'),
        ('usuario', 'Usuário Comum'),
    ]
    
    nome_completo = models.CharField(max_length=255, verbose_name="Nome Completo", blank=True)
    telefone = models.CharField(max_length=20, verbose_name="Telefone", blank=True)
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF", null=True, blank=True)
    tipo_usuario = models.CharField(max_length=15, choices=STATUS_CHOICES, default='usuario', verbose_name="Tipo de Usuário")

    def __str__(self):
        return f"{self.username} ({self.get_tipo_usuario_display()})"