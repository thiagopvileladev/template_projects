"""
Models do acervo musical — docs/banco-de-dados/modelo_de_dados.md.

Campos acrescentados em relação ao DER da Fase 1 (genero, bpm, popularidade,
spotify_id da faixa) estão justificados em docs/fase2/mudancas_fase1.md.
"""

from datetime import date

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.urls import reverse

NOTA_VALIDATORS = [MinValueValidator(0.0), MaxValueValidator(10.0)]


def ano_maximo():
    return date.today().year + 1


class Album(models.Model):
    titulo = models.CharField('título', max_length=200)
    artista = models.CharField(max_length=200)
    ano_lancamento = models.PositiveSmallIntegerField(
        'ano de lançamento',
        null=True,
        blank=True,
        validators=[MinValueValidator(1900)],
    )
    capa_url = models.URLField('URL da capa', blank=True)
    spotify_id = models.CharField(
        'ID no Spotify', max_length=64, unique=True, null=True, blank=True
    )

    class Meta:
        ordering = ['artista', 'titulo']
        verbose_name = 'álbum'
        verbose_name_plural = 'álbuns'

    def __str__(self):
        return f'{self.titulo} — {self.artista}'

    def get_absolute_url(self):
        return reverse('acervo:album_detalhe', args=[self.pk])

    def clean(self):
        if self.ano_lancamento and self.ano_lancamento > ano_maximo():
            raise ValidationError(
                {'ano_lancamento': 'O ano de lançamento não pode estar no futuro.'}
            )


class Faixa(models.Model):
    class Genero(models.TextChoices):
        ROCK = 'rock', 'Rock'
        POP = 'pop', 'Pop'
        HIP_HOP = 'hip_hop', 'Hip-Hop / Rap'
        ELETRONICA = 'eletronica', 'Eletrônica'
        JAZZ = 'jazz', 'Jazz'
        BLUES = 'blues', 'Blues'
        CLASSICA = 'classica', 'Clássica'
        MPB = 'mpb', 'MPB'
        SAMBA = 'samba', 'Samba / Pagode'
        SERTANEJO = 'sertanejo', 'Sertanejo'
        FUNK = 'funk', 'Funk'
        RNB = 'rnb', 'R&B / Soul'
        REGGAE = 'reggae', 'Reggae'
        METAL = 'metal', 'Metal'
        INDIE = 'indie', 'Indie / Alternativo'
        OUTRO = 'outro', 'Outro'

    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, related_name='faixas', verbose_name='álbum'
    )
    titulo = models.CharField('título', max_length=200)
    duracao_ms = models.PositiveIntegerField('duração (ms)', null=True, blank=True)
    isrc = models.CharField(
        'ISRC',
        max_length=12,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                r'^[A-Z]{2}[A-Z0-9]{3}\d{7}$',
                'ISRC inválido. Formato esperado: 12 caracteres, ex.: GBUM71029604.',
            )
        ],
    )
    genero = models.CharField(
        'gênero', max_length=20, choices=Genero.choices, default=Genero.OUTRO
    )
    bpm = models.PositiveSmallIntegerField(
        'BPM',
        null=True,
        blank=True,
        validators=[MinValueValidator(20), MaxValueValidator(300)],
    )
    popularidade = models.PositiveSmallIntegerField(
        null=True, blank=True, validators=[MaxValueValidator(100)]
    )
    spotify_id = models.CharField(
        'ID no Spotify', max_length=64, unique=True, null=True, blank=True
    )

    class Meta:
        ordering = ['album', 'titulo']

    def __str__(self):
        return f'{self.titulo} ({self.album.artista})'

    def get_absolute_url(self):
        return reverse('acervo:faixa_detalhe', args=[self.pk])

    @property
    def artista(self):
        return self.album.artista


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        verbose_name='usuário',
    )
    faixa = models.ForeignKey(
        Faixa, on_delete=models.CASCADE, related_name='avaliacoes'
    )
    nota_pitchfork = models.FloatField(
        'nota Pitchfork', null=True, blank=True, validators=NOTA_VALIDATORS
    )
    nota_pessoal = models.FloatField('nota pessoal', validators=NOTA_VALIDATORS)
    resenha = models.TextField(blank=True)
    criado_em = models.DateTimeField('criado em', auto_now_add=True)

    class Meta:
        ordering = ['-criado_em']
        verbose_name = 'avaliação'
        verbose_name_plural = 'avaliações'
        constraints = [
            # Cada curador avalia uma faixa uma única vez (pode editar depois).
            models.UniqueConstraint(
                fields=['usuario', 'faixa'], name='avaliacao_unica_por_usuario'
            ),
            models.CheckConstraint(
                condition=models.Q(nota_pessoal__gte=0, nota_pessoal__lte=10),
                name='nota_pessoal_entre_0_e_10',
            ),
        ]

    def __str__(self):
        return f'{self.faixa} — {self.nota_pessoal}'


class Colecao(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='colecoes',
        verbose_name='usuário',
    )
    nome = models.CharField(max_length=120)
    descricao = models.CharField('descrição', max_length=500, blank=True)
    is_publica = models.BooleanField('pública', default=False)
    # Relacionamento N:N do DER (FAIXA }|--|{ COLECAO).
    # O Django cria a tabela intermediária acervo_colecao_faixas.
    faixas = models.ManyToManyField(Faixa, related_name='colecoes', blank=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'coleção'
        verbose_name_plural = 'coleções'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'nome'], name='colecao_nome_unico_por_usuario'
            ),
        ]

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('acervo:colecao_detalhe', args=[self.pk])

    def capas_mosaico(self):
        """Até 4 capas diferentes das faixas, para o mosaico (como playlists).

        Usa self.faixas.all(), aproveitando o prefetch_related das views.
        """
        capas = []
        for faixa in self.faixas.all():
            capa = faixa.album.capa_url
            if capa and capa not in capas:
                capas.append(capa)
                if len(capas) == 4:
                    break
        # Mosaico 2x2 precisa de 4; com menos, mostra só a primeira capa inteira.
        return capas if len(capas) == 4 else capas[:1]
