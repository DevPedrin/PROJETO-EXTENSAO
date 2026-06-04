from django.contrib import admin
from .models import Delegacia, Denuncia, AnexoDenuncia, VideoEducativo

class AnexoDenunciaInline(admin.TabularInline):
    model = AnexoDenuncia
    extra = 0

@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'delegacia', 'status', 'data_criacao', 'anonimo')
    list_filter = ('status', 'data_criacao', 'anonimo', 'delegacia')
    search_fields = ('titulo', 'descricao', 'autor__username')
    inlines = [AnexoDenunciaInline]
    actions = ['aprovar_denuncias', 'rejeitar_denuncias']

    def aprovar_denuncias(self, request, queryset):
        queryset.update(status='APROVADA')
    aprovar_denuncias.short_description = "Aprovar denúncias selecionadas"

    def rejeitar_denuncias(self, request, queryset):
        queryset.update(status='REJEITADA')
    rejeitar_denuncias.short_description = "Rejeitar denúncias selecionadas"

@admin.register(Delegacia)
class DelegaciaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'telefone')
    list_filter = ('tipo',)
    search_fields = ('nome', 'endereco')

@admin.register(VideoEducativo)
class VideoEducativoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem')
    search_fields = ('titulo',)
