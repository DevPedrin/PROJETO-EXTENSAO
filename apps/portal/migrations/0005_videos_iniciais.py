from django.db import migrations


def criar_videos_iniciais(apps, schema_editor):
    Video = apps.get_model('portal', 'Video')
    videos = [
        {
            'titulo': 'Como se proteger do Golpe do WhatsApp',
            'descricao': 'Aprenda as principais táticas utilizadas por criminosos e ative a confirmação em duas etapas para proteger sua conta.',
            'url_youtube': 'https://www.youtube.com/watch?v=1hcwBhtdznw'
        },
        {
            'titulo': 'Cuidado com o Golpe do Falso Funcionário de Banco',
            'descricao': 'Entenda como engenharia social é utilizada para clonar cartões e roubar senhas através de ligações falsas de suporte.',
            'url_youtube': 'https://www.youtube.com/watch?v=JEP9pmN2GEM'
        },
        {
            'titulo': 'Golpe do Pix: Conheça as novas modalidades',
            'descricao': 'Fique atento ao Pix agendado, falsos comprovantes e saiba o que fazer se você cair em uma armadilha financeira.',
            'url_youtube': 'https://www.youtube.com/watch?v=KE0V2WaF0qU'
        },
        {
            'titulo': 'Links e Promoções Falsas: Como identificar Phishing',
            'descricao': 'Dicas essenciais para validar URLs, checar sites oficiais e não clicar em links maliciosos recebidos por SMS ou redes sociais.',
            'url_youtube': 'https://www.youtube.com/watch?v=C6-RGQZae90'
        },
    ]
    for dados in videos:
        if not Video.objects.filter(url_youtube=dados['url_youtube']).exists():
            Video.objects.create(**dados)


def remover_videos_iniciais(apps, schema_editor):
    Video = apps.get_model('portal', 'Video')
    urls = [
        'https://www.youtube.com/watch?v=1hcwBhtdznw',
        'https://www.youtube.com/watch?v=JEP9pmN2GEM',
        'https://www.youtube.com/watch?v=KE0V2WaF0qU',
        'https://www.youtube.com/watch?v=C6-RGQZae90',
    ]
    Video.objects.filter(url_youtube__in=urls).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_delegacias_iniciais'),
    ]

    operations = [
        migrations.RunPython(
            criar_videos_iniciais,
            reverse_code=remover_videos_iniciais
        ),
    ]