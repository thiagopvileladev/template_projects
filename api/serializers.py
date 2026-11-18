"""
Serializers: convertem os models em JSON e validam o JSON recebido.

Dados pessoais dos usuários (e-mail) nunca são expostos: avaliações e
coleções mostram apenas o nome de usuário.
"""

from django.contrib.auth import authenticate
from rest_framework import serializers

from acervo.models import Album, Avaliacao, Colecao, Faixa


class FaixaResumoSerializer(serializers.ModelSerializer):
    artista = serializers.CharField(source='album.artista', read_only=True)
    genero = serializers.CharField(source='get_genero_display', read_only=True)

    class Meta:
        model = Faixa
        fields = ('id', 'titulo', 'artista', 'genero', 'bpm')


class FaixaSerializer(serializers.ModelSerializer):
    artista = serializers.CharField(source='album.artista', read_only=True)
    album = serializers.SerializerMethodField()
    genero = serializers.CharField(source='get_genero_display', read_only=True)
    genero_codigo = serializers.CharField(source='genero', read_only=True)
    media_notas = serializers.SerializerMethodField()

    class Meta:
        model = Faixa
        fields = ('id', 'titulo', 'artista', 'album', 'genero', 'genero_codigo', 'bpm',
                  'duracao_ms', 'isrc', 'popularidade', 'spotify_id', 'media_notas')

    def get_album(self, faixa) -> dict:
        return {'id': faixa.album_id, 'titulo': faixa.album.titulo, 'capa_url': faixa.album.capa_url}

    def get_media_notas(self, faixa) -> float | None:
        media = getattr(faixa, 'media', None)
        return round(media, 2) if media is not None else None


class AlbumSerializer(serializers.ModelSerializer):
    total_faixas = serializers.IntegerField(read_only=True)

    class Meta:
        model = Album
        fields = ('id', 'titulo', 'artista', 'ano_lancamento', 'capa_url', 'spotify_id', 'total_faixas')


class AlbumDetalheSerializer(AlbumSerializer):
    faixas = FaixaResumoSerializer(many=True, read_only=True)

    class Meta(AlbumSerializer.Meta):
        fields = AlbumSerializer.Meta.fields + ('faixas',)


class AvaliacaoSerializer(serializers.ModelSerializer):
    faixa_id = serializers.PrimaryKeyRelatedField(source='faixa', queryset=Faixa.objects.all())
    usuario = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = Avaliacao
        fields = ('id', 'faixa_id', 'usuario', 'nota_pessoal', 'nota_pitchfork', 'resenha', 'criado_em')
        read_only_fields = ('id', 'usuario', 'criado_em')

    def validate(self, dados):
        # Uma avaliação por usuário e faixa (regra do modelo de dados).
        faixa = dados.get('faixa') or getattr(self.instance, 'faixa', None)
        usuario = self.context['request'].user
        repetida = Avaliacao.objects.filter(usuario=usuario, faixa=faixa)
        if self.instance:
            repetida = repetida.exclude(pk=self.instance.pk)
        if repetida.exists():
            raise serializers.ValidationError(
                {'faixa_id': 'Você já avaliou esta faixa. Use PUT/PATCH para alterar a avaliação.'}
            )
        return dados


class ColecaoSerializer(serializers.ModelSerializer):
    usuario = serializers.CharField(source='usuario.username', read_only=True)
    faixas = FaixaResumoSerializer(many=True, read_only=True)

    class Meta:
        model = Colecao
        fields = ('id', 'nome', 'descricao', 'usuario', 'faixas')


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False, write_only=True)

    def validate(self, dados):
        usuario = authenticate(
            request=self.context.get('request'),
            username=dados['email'].strip().lower(),
            password=dados['password'],
        )
        if not usuario:
            raise serializers.ValidationError('E-mail ou senha incorretos.', code='authorization')
        dados['usuario'] = usuario
        return dados


class TokenRespostaSerializer(serializers.Serializer):
    token = serializers.CharField()
