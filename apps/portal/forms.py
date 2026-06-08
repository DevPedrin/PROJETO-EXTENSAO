from django import forms
from .models import Denuncia


class DenunciaForm(forms.ModelForm):
    """
    Formulário de denúncia.

    Segurança:
        Os campos `usuario` e `criado_em` são EXCLUÍDOS intencionalmente.
        Eles nunca devem vir do cliente — são definidos exclusivamente
        na view, após validação da autenticação e da flag `anonima`.

        Mesmo que alguém injete manualmente `usuario` no corpo da
        requisição POST, o Django ignorará o campo por não estar em `fields`.
    """

    class Meta:
        model = Denuncia
        fields = [
            'tipo_golpe',
            'data_ocorrencia',
            'cidade',
            'descricao',
            'nome_informado',
            'faixa_etaria',
            'anonima',
        ]
        widgets = {
            'tipo_golpe': forms.Select(attrs={
                'id': 'form-tipo-golpe',
            }),
            'data_ocorrencia': forms.DateInput(attrs={
                'type': 'date',
                'id': 'form-data',
            }),
            'cidade': forms.TextInput(attrs={
                'id': 'form-cidade',
                'placeholder': 'Ex.: Palmas — TO',
            }),
            'descricao': forms.Textarea(attrs={
                'id': 'form-descricao',
                'placeholder': (
                    'Descreva brevemente o que aconteceu. '
                    'Quanto mais detalhes, melhor para o mapeamento...'
                ),
                'rows': 4,
            }),
            'nome_informado': forms.TextInput(attrs={
                'id': 'form-nome',
                'placeholder': 'Pode deixar em branco',
            }),
            'faixa_etaria': forms.Select(attrs={
                'id': 'form-idade',
            }),
            'anonima': forms.CheckboxInput(attrs={
                'id': 'form-anonimo',
                'style': 'width: auto; cursor: pointer;',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        # Garante que `descricao` e `tipo_golpe` estão presentes
        descricao = cleaned_data.get('descricao', '').strip()
        tipo_golpe = cleaned_data.get('tipo_golpe', '').strip()

        if not descricao:
            self.add_error('descricao', 'A descrição do ocorrido é obrigatória.')

        if not tipo_golpe:
            self.add_error('tipo_golpe', 'Selecione o tipo de golpe.')

        return cleaned_data
