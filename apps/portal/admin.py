from django.contrib import admin

from .models import Denuncia, Delegacia, Video


@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):

    list_display = (
        'protocolo',
        'tipo_golpe',
        'status',
        'publicada',
        'anonima',
        'cidade',
        'criado_em',
    )

    list_filter = (
        'status',
        'publicada',
        'anonima',
        'tipo_golpe',
        'criado_em',
    )

    search_fields = (
        'protocolo',
        'cidade',
        'descricao',
    )

    ordering = (
        '-criado_em',
    )

    date_hierarchy = 'criado_em'

    readonly_fields = (
        'protocolo',
        'autor_hash',
        'criado_em',
        'atualizado_em',
        'moderado_em',
        'publicada_em',
    )

    fieldsets = (
        ('Identificação', {
            'fields': (
                'protocolo',
                'anonima',
                'autor_hash',
            )
        }),

        ('Denúncia', {
            'fields': (
                'tipo_golpe',
                'data_ocorrencia',
                'cidade',
                'descricao',
            )
        }),

        ('Moderação', {
            'fields': (
                'status',
                'moderado_por',
                'moderado_em',
                'motivo_moderacao',
            )
        }),

        ('Publicação', {
            'fields': (
                'publicada',
                'publicada_em',
            )
        }),

        ('Auditoria', {
            'fields': (
                'criado_em',
                'atualizado_em',
            )
        }),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = (
        'titulo',
        'criado_em',
    )

    search_fields = (
        'titulo',
        'descricao',
    )


@admin.register(Delegacia)
class DelegaciaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'tipo',
        'cidade',
        'ativo',
    )

    list_filter = (
        'tipo',
        'ativo',
    )

    search_fields = (
        'nome',
        'cidade',
    )