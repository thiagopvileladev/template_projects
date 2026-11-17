from django.contrib import admin

from .models import Album, Avaliacao, Colecao, Faixa


class FaixaInline(admin.TabularInline):
    model = Faixa
    extra = 0
    fields = ('titulo', 'genero', 'bpm', 'isrc')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'artista', 'ano_lancamento')
    search_fields = ('titulo', 'artista')
    inlines = [FaixaInline]


@admin.register(Faixa)
class FaixaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'album', 'genero', 'bpm', 'popularidade')
    list_filter = ('genero',)
    search_fields = ('titulo', 'album__artista', 'isrc')


@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('faixa', 'usuario', 'nota_pessoal', 'nota_pitchfork', 'criado_em')
    list_filter = ('usuario',)


@admin.register(Colecao)
class ColecaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'usuario', 'is_publica')
    filter_horizontal = ('faixas',)
