from django import forms

from .models import Album, Avaliacao, Colecao, Faixa


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ('titulo', 'artista', 'ano_lancamento', 'capa_url')


class FaixaForm(forms.ModelForm):
    class Meta:
        model = Faixa
        fields = ('album', 'titulo', 'genero', 'bpm', 'duracao_ms', 'isrc', 'popularidade')
        help_texts = {
            'bpm': 'Andamento em batidas por minuto (20 a 300).',
            'duracao_ms': 'Duração em milissegundos (ex.: 3:30 = 210000).',
            'popularidade': 'De 0 a 100, preenchido pelo Spotify quando importado.',
        }

    def clean_isrc(self):
        # ISRC vazio vira NULL: o campo é único e vários "" dariam conflito.
        isrc = (self.cleaned_data.get('isrc') or '').strip().upper()
        return isrc or None


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ('nota_pessoal', 'nota_pitchfork', 'resenha')
        widgets = {
            'nota_pessoal': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 10}),
            'nota_pitchfork': forms.NumberInput(attrs={'step': '0.1', 'min': 0, 'max': 10}),
            'resenha': forms.Textarea(attrs={'rows': 5}),
        }


class ColecaoForm(forms.ModelForm):
    class Meta:
        model = Colecao
        fields = ('nome', 'descricao', 'is_publica', 'faixas')
        widgets = {'faixas': forms.CheckboxSelectMultiple}

    def __init__(self, *args, usuario, **kwargs):
        # O usuário vem da view: necessário para validar nome único por usuário.
        self.usuario = usuario
        super().__init__(*args, **kwargs)
        self.fields['faixas'].queryset = Faixa.objects.select_related('album')

    def clean_nome(self):
        nome = self.cleaned_data['nome'].strip()
        repetida = Colecao.objects.filter(usuario=self.usuario, nome__iexact=nome)
        if self.instance.pk:
            repetida = repetida.exclude(pk=self.instance.pk)
        if repetida.exists():
            raise forms.ValidationError('Você já tem uma coleção com este nome.')
        return nome
