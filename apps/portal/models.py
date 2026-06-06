from django.db import models
from django.conf import settings

class Delegacia(models.Model):
    TIPOS_CHOICES = [
        ('CIVIL', 'Civil'),
        ('MILITAR', 'Militar'),
        ('MULHER', 'Delegacia da Mulher'),
        ('CRIANÇA_ADOLESCENTE', 'Delegacia da Criança e Adolescente'),
        ('OUTRO', 'Outro'),
    ]
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPOS_CHOICES)
    endereco = models.TextField(blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Denuncia(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADA', 'Aprovada'),
        ('REJEITADA', 'Rejeitada'),
    ]
    titulo = models.CharField(max_length=200, blank=True, null=True)
    descricao = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    anonimo = models.BooleanField(default=False)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='denuncias')
    delegacia = models.ForeignKey(Delegacia, on_delete=models.SET_NULL, null=True, blank=True, related_name='denuncias')

    def __str__(self):
        return self.titulo or f"Denúncia #{self.id}"

class AnexoDenuncia(models.Model):
    denuncia = models.ForeignKey(Denuncia, on_delete=models.CASCADE, related_name='anexos')
    arquivo = models.FileField(upload_to='denuncias/anexos/')

    def __str__(self):
        return f"Anexo de {self.denuncia}"

class VideoEducativo(models.Model):
    titulo = models.CharField(max_length=200)
    link_externo = models.URLField()
    data_postagem = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
