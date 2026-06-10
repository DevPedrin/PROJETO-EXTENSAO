from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class Denuncia(models.Model):

    TIPOS_GOLPE = [
        ('whatsapp_redes', 'Golpe do WhatsApp / Redes Sociais'),
        ('falso_banco', 'Falso funcionário de banco'),
        ('pix', 'Golpe do Pix'),
        ('promocao_falsa', 'Promoção ou Prêmio falso'),
        ('link_falso', 'Link ou página falsa'),
        ('outro', 'Outro'),
    ]

    STATUS_DENUNCIA = [
        ('analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    FAIXAS_ETARIAS = [
        ('18_25', '18 a 25 anos'),
        ('26_35', '26 a 35 anos'),
        ('36_50', '36 a 50 anos'),
        ('51_65', '51 a 65 anos'),
        ('65_mais', 'Acima de 65 anos'),
    ]

    protocolo = models.CharField(
        max_length=30,
        unique=True,
        editable=False,
        verbose_name='Protocolo'
    )

    anonima = models.BooleanField(
        default=False,
        verbose_name='Denúncia anônima'
    )

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='denuncias',
        verbose_name='Usuário'
    )

    autor_hash = models.CharField(
        max_length=64,
        blank=True,
        editable=False,
        db_index=True,
        verbose_name='Identificador do autor'
    )

    tipo_golpe = models.CharField(
        max_length=30,
        choices=TIPOS_GOLPE,
        verbose_name='Tipo de golpe'
    )

    faixa_etaria = models.CharField(
        max_length=10,
        choices=FAIXAS_ETARIAS,
        blank=True,
        verbose_name='Faixa etária'
    )

    data_ocorrencia = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data da ocorrência'
    )


    cidade = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Cidade'
    )

    descricao = models.TextField(
        verbose_name='Descrição'
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_DENUNCIA,
        default='analise',
        verbose_name='Status'
    )

    moderado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='denuncias_moderadas',
        verbose_name='Moderado por'
    )

    moderado_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da moderação'
    )

    motivo_moderacao = models.TextField(
        blank=True,
        verbose_name='Motivo da decisão'
    )

    publicada = models.BooleanField(
        default=False,
        verbose_name='Publicada'
    )

    publicada_em = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Data da publicação'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['-criado_em']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['criado_em']),
            models.Index(fields=['autor_hash']),
        ]

    def save(self, *args, **kwargs):
        if not self.protocolo:
            ano = timezone.now().year
            codigo = uuid.uuid4().hex[:6].upper()
            self.protocolo = f'DEN-{ano}-{codigo}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.protocolo} - {self.get_tipo_golpe_display()}'

    @property
    def exibir_autor(self):
        return 'Anônimo' if self.anonima else 'Identificado'
    
    @property
    def nome_autor(self):
        if self.anonima or not self.usuario:
            return 'Anônimo'
        return self.usuario.nome_completo or self.usuario.username

    @property
    def pode_ser_moderada(self):
        return self.status == 'analise'

    @property
    def foi_aprovada(self):
        return self.status == 'aprovada'

    @property
    def foi_rejeitada(self):
        return self.status == 'rejeitada'

    @property
    def esta_publicada(self):
        return self.publicada
    
    


class Video(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    url_youtube = models.URLField(verbose_name="Link do Vídeo")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    @property
    def thumbnail_url(self):
        import re

        reg_exp = r'^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*'
        match = re.match(reg_exp, self.url_youtube)

        if match and len(match.group(2)) == 11:
            return f"https://img.youtube.com/vi/{match.group(2)}/mqdefault.jpg"

        return ""


class Delegacia(models.Model):

    TIPOS = [
        ('Ciberneticos', 'Delegacia de Crimes Cibernéticos'),
        ('Idoso', 'Delegacia de Atendimento ao Idoso'),
        ('Procon', 'Procon'),
        ('Canal Online', 'Canal Online'),
    ]

    nome = models.CharField(max_length=200, verbose_name='Nome')

    tipo = models.CharField(
        max_length=20,
        choices=TIPOS,
        verbose_name='Tipo'
    )

    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cidade'
    )

    endereco = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Endereço'
    )

    telefone = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Telefone'
    )

    horario = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Horário'
    )

    url = models.URLField(
        blank=True,
        verbose_name='Link'
    )

    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    class Meta:
        verbose_name = 'Delegacia / Órgão'
        verbose_name_plural = 'Delegacias / Órgãos'
        ordering = ['cidade', 'nome']

    def __str__(self):
        return f'{self.nome} - {self.cidade}' if self.cidade else self.nome