from django.db import models
from django.conf import settings

class Video(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descricao = models.TextField(verbose_name="Descrição", blank=True)
    url_youtube = models.URLField(verbose_name="Link do Vídeo (YouTube, etc.)")
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Denuncia(models.Model):
    """
    Model que representa uma denúncia de golpe digital.

    Regra de anonimato:
        Quando `anonima=True`, o campo `usuario` aponta SEMPRE para o
        usuário técnico fixo (anonimo_sistema), independentemente de quem
        esteja autenticado. Essa lógica é garantida exclusivamente no backend
        (view), nunca no frontend.
    """

    TIPOS_GOLPE = [
        ('whatsapp_redes', 'Golpe do WhatsApp / Redes Sociais'),
        ('falso_banco', 'Falso funcionário de banco'),
        ('pix', 'Golpe do Pix'),
        ('promocao_falsa', 'Promoção ou Prêmio falso'),
        ('link_falso', 'Link ou página falsa'),
        ('outro', 'Outro'),
    ]

    FAIXAS_ETARIAS = [
        ('18_29', '18 a 29 anos'),
        ('30_44', '30 a 44 anos'),
        ('45_59', '45 a 59 anos'),
        ('60_mais', '60 anos ou mais'),
    ]

    STATUS_DENUNCIA = [
        ('analise', 'Em Análise'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='denuncias',
        verbose_name='Usuário',
        help_text=(
            'Para denúncias anônimas, aponta para o usuário técnico '
            '"anonimo_sistema" — nunca para o usuário real autenticado.'
        ),
    )

    anonima = models.BooleanField(
        default=False,
        verbose_name='Denúncia anônima',
        help_text=(
            'Se True, o usuário real NÃO é rastreável. '
            'O campo "usuario" aponta para o usuário técnico fixo.'
        ),
    )

    tipo_golpe = models.CharField(
        max_length=30,
        choices=TIPOS_GOLPE,
        verbose_name='Tipo de golpe',
    )

    data_ocorrencia = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data da ocorrência',
    )

    cidade = models.CharField(
        max_length=120,
        blank=True,
        verbose_name='Cidade',
    )

    descricao = models.TextField(
        verbose_name='Descrição do ocorrido',
        help_text='Descrição fornecida pelo denunciante.',
    )

    nome_informado = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Nome informado (opcional)',
        help_text='Nome fornecido voluntariamente no formulário, se houver.',
    )

    faixa_etaria = models.CharField(
        max_length=10,
        choices=FAIXAS_ETARIAS,
        blank=True,
        verbose_name='Faixa etária',
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_DENUNCIA,
        default='analise',
        verbose_name='Status da Denúncia'
    )

    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Registrado em',
    )

    class Meta:
        verbose_name = 'Denúncia'
        verbose_name_plural = 'Denúncias'
        ordering = ['-criado_em']

    def __str__(self):
        tipo = self.get_tipo_golpe_display()
        status = 'Anônima' if self.anonima else f'por {self.usuario.username}'
        return f'[{self.pk}] {tipo} — {status} ({self.criado_em:%d/%m/%Y})'

    @property
    def exibir_autor(self):
        if self.anonima:
            return 'Anônimo'
        return self.usuario.username
    
class Delegacia(models.Model):
    TIPOS = [
        ('Ciberneticos', 'Delegacia de Crimes Cibernéticos'),
        ('Idoso', 'Delegacia de Atendimento ao Idoso'),
        ('Procon', 'Procon'),
        ('Canal Online', 'Canal Online'),
    ]

    nome = models.CharField(max_length=200, verbose_name='Nome')
    tipo = models.CharField(max_length=20, choices=TIPOS, verbose_name='Tipo')
    cidade = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Cidade',
        help_text='Deixe em branco para canais online/nacionais.',
    )
    endereco = models.CharField(max_length=255, blank=True, verbose_name='Endereço')
    telefone = models.CharField(max_length=50, blank=True, verbose_name='Telefone')
    horario = models.CharField(max_length=100, blank=True, verbose_name='Horário de funcionamento')
    url = models.URLField(blank=True, verbose_name='Link (para canais online)')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Delegacia / Órgão'
        verbose_name_plural = 'Delegacias / Órgãos'
        ordering = ['cidade', 'nome']

    def __str__(self):
        cidade_str = f' — {self.cidade}' if self.cidade else ''
        return f'{self.nome}{cidade_str}'