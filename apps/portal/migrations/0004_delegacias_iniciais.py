from django.db import migrations


def criar_delegacias_iniciais(apps, schema_editor):
    Delegacia = apps.get_model('portal', 'Delegacia')
    delegacias = [
        {
            'nome': 'Delegacia de Crimes Cibernéticos de Palmas',
            'tipo': 'Ciberneticos',
            'cidade': 'Palmas',
            'endereco': 'Avenida Teotônio Segurado, Centro',
            'telefone': '(63) 3218-0000',
            'horario': '08:00 às 18:00',
            'url': '',
            'ativo': True
        },
        {
            'nome': 'Delegacia de Atendimento ao Idoso',
            'tipo': 'Idoso',
            'cidade': 'Palmas',
            'endereco': 'Quadra 602 Sul, ACSU-SE 60',
            'telefone': '(63) 3218-1111',
            'horario': '08:00 às 18:00',
            'url': '',
            'ativo': True
        },
        {
            'nome': 'Procon Tocantins',
            'tipo': 'Procon',
            'cidade': 'Palmas',
            'endereco': 'Quadra 104 Sul, Rua SE 09',
            'telefone': '151',
            'horario': '08:00 às 18:00',
            'url': 'https://procon.to.gov.br/',
            'ativo': True
        },
        {
            'nome': 'Canal Online de Denúncias',
            'tipo': 'Canal Online',
            'cidade': '',
            'endereco': '',
            'telefone': '',
            'horario': '24 Horas',
            'url': 'https://www.gov.br/disque100',
            'ativo': True
        },
    ]
    for dados in delegacias:
        if not Delegacia.objects.filter(nome=dados['nome'], cidade=dados['cidade']).exists():
            Delegacia.objects.create(**dados)


def remover_delegacias_iniciais(apps, schema_editor):
    Delegacia = apps.get_model('portal', 'Delegacia')
    Delegacia.objects.filter(
        tipo__in=['Ciberneticos', 'Idoso', 'Procon', 'Canal Online']
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_denuncia_usuario'),
    ]

    operations = [
        migrations.RunPython(
            criar_delegacias_iniciais,
            reverse_code=remover_delegacias_iniciais
        ),
    ]