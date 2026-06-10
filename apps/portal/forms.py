from django import forms
from .models import Denuncia, Delegacia


class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = [
            'tipo_golpe',
            'data_ocorrencia',
            'cidade',
            'descricao',
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
                'placeholder': 'Ex.: Palmas - TO',
            }),

            'descricao': forms.Textarea(attrs={
                'id': 'form-descricao',
                'rows': 5,
                'placeholder': (
                    'Descreva o ocorrido com o máximo de detalhes possível.'
                )
            }),

            'anonima': forms.CheckboxInput(attrs={
                'id': 'form-anonimo',
                'style': 'width:auto;cursor:pointer;'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()

        descricao = cleaned_data.get('descricao')
        tipo_golpe = cleaned_data.get('tipo_golpe')

        if not descricao:
            self.add_error(
                'descricao',
                'A descrição é obrigatória.'
            )

        if not tipo_golpe:
            self.add_error(
                'tipo_golpe',
                'Selecione um tipo de golpe.'
            )

        return cleaned_data


class DelegaciaForm(forms.ModelForm):

    class Meta:
        model = Delegacia

        fields = [
            'nome',
            'tipo',
            'cidade',
            'endereco',
            'telefone',
            'horario',
            'url',
            'ativo',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),

            'cidade': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'endereco': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'telefone': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'horario': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'url': forms.URLInput(attrs={
                'class': 'form-control'
            }),

            'ativo': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }