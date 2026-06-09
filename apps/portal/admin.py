from django.contrib import admin
from django.conf import settings
from .models import Denuncia, Delegacia


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    """
    Painel administrativo de denúncias.

    Segurança:
        - Para denúncias anônimas, o campo `usuario` aponta para o usuário
          técnico 'anonimo_sistema' — nunca para o usuário real.
        - O campo `usuario` é somente leitura no detail, exibindo
          'Anônimo' quando `anonima=True`, via método `autor_display`.
        - Nenhum campo revela o autor real de uma denúncia anônima.
    """

    # ─── Listagem ─────────────────────────────────────────────────────────────
    list_display = [
        'pk',
        'tipo_golpe',
        'cidade',
        'faixa_etaria',
        'anonima',
        'autor_display',
        'criado_em',
    ]
    list_filter = [
        'anonima',
        'tipo_golpe',
        'faixa_etaria',
        'criado_em',
    ]
    search_fields = ['descricao', 'cidade', 'nome_informado']
    ordering = ['-criado_em']
    date_hierarchy = 'criado_em'

    # ─── Detalhe ──────────────────────────────────────────────────────────────
    readonly_fields = [
        'autor_display',   # exibe 'Anônimo' ou o username
        'criado_em',
    ]

    fieldsets = (
        ('Identificação', {
            'fields': ('anonima', 'autor_display', 'criado_em'),
        }),
        ('Dados da Ocorrência', {
            'fields': (
                'tipo_golpe',
                'data_ocorrencia',
                'cidade',
                'descricao',
            ),
        }),
        ('Dados Opcionais do Relato', {
            'fields': ('nome_informado', 'faixa_etaria'),
            'classes': ('collapse',),
        }),
    )

    # ─── Campo usuario excluído do form ──────────────────────────────────────
    # O campo `usuario` não aparece como editável para EVITAR que um admin
    # acidentalmente altere o vínculo e quebre a garantia de anonimato.
    exclude = ['usuario']

    # ─── Método seguro de exibição do autor ──────────────────────────────────
    @admin.display(description='Autor', ordering='usuario__username')
    def autor_display(self, obj):
        return obj.exibir_autor

    # ─── Impede criação manual de denúncias pelo admin ───────────────────────
    def has_add_permission(self, request):
        """
        Denúncias só podem ser criadas via formulário público (com a
        lógica de anonimato da view). Criar via admin pularia essa lógica.
        """
        return False


@admin.register(Delegacia)
class DelegaciaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'cidade', 'telefone', 'ativo']
    list_filter = ['tipo', 'cidade', 'ativo']
    search_fields = ['nome', 'cidade', 'endereco']
    list_editable = ['ativo']
