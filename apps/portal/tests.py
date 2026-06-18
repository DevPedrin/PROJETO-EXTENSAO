from django.test import TestCase

from .forms import DenunciaForm


class DenunciaFormTests(TestCase):

    def test_data_ocorrencia_field_retains_submitted_date(self):
        form = DenunciaForm({
            'tipo_golpe': 'pix',
            'data_ocorrencia': '2025-07-04',
            'cidade': 'Palmas — TO',
            'descricao': 'Teste de data',
            'anonima': 'on',
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['data_ocorrencia'].isoformat(), '2025-07-04')
