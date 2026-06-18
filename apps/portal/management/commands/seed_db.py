from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from faker import Faker
import random

from apps.portal.models import Denuncia, Video, Delegacia


class Command(BaseCommand):
    help = 'Popula o banco de dados com usuários, denúncias, vídeos e delegacias de exemplo.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=30,
            help='Quantidade de usuários fictícios a criar (exclui admin/moderador/usuario iniciais).'
        )
        parser.add_argument(
            '--denuncias',
            type=int,
            default=80,
            help='Quantidade de denúncias fictícias a criar.'
        )
        parser.add_argument(
            '--videos',
            type=int,
            default=10,
            help='Quantidade de vídeos fictícios a criar.'
        )
        parser.add_argument(
            '--delegacias',
            type=int,
            default=12,
            help='Quantidade de delegacias fictícias a criar.'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Limpa todos os vídeos e delegacias antes de popular (preserva dados das migrations por padrão).'
        )

    def handle(self, *args, **options):
        faker = Faker('pt_BR')
        User = get_user_model()
        reset = options.get('reset', False)

        if reset:
            self.stdout.write(self.style.WARNING('Limpando dados existentes...'))
            Delegacia.objects.all().delete()
            Video.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('  Dados de delegacias e vídeos removidos.'))

        self.stdout.write(self.style.MIGRATE_HEADING('Populando usuários...'))
        self._create_users(User, faker, options['users'])

        self.stdout.write(self.style.MIGRATE_HEADING('Populando delegacias...'))
        self._create_delegacias(faker, options['delegacias'])

        self.stdout.write(self.style.MIGRATE_HEADING('Populando vídeos...'))
        self._create_videos(faker, options['videos'])

        self.stdout.write(self.style.MIGRATE_HEADING('Populando denúncias...'))
        self._create_denuncias(User, faker, options['denuncias'])

        self.stdout.write(self.style.SUCCESS('Seed concluído com sucesso.'))

    def _create_users(self, User, faker, count):
        status_choices = ['usuario', 'moderador', 'admin']
        existing_usernames = set(User.objects.values_list('username', flat=True))
        existing_emails = set(User.objects.values_list('email', flat=True))
        created = 0
        max_attempts = count * 4

        while created < count and max_attempts > 0:
            max_attempts -= 1
            username = faker.unique.user_name()
            email = faker.unique.email()
            nome_completo = faker.name()
            telefone = faker.phone_number()
            cpf = self._generate_cpf()
            tipo_usuario = random.choices(status_choices, weights=[85, 10, 5], k=1)[0]

            if username in existing_usernames or email in existing_emails:
                continue

            user = User.objects.create_user(
                username=username,
                email=email,
                password='senha123',
                nome_completo=nome_completo,
                telefone=telefone,
                cpf=cpf,
                tipo_usuario=tipo_usuario,
                is_active=True,
            )

            if tipo_usuario == 'admin':
                user.is_staff = True
                user.is_superuser = False
                user.save()

            existing_usernames.add(username)
            existing_emails.add(email)
            created += 1

        self.stdout.write(f'  Usuários criados: {created}')

    def _create_delegacias(self, faker, count):
        tipos = ['Ciberneticos', 'Idoso', 'Procon', 'Canal Online']
        for _ in range(count):
            nome = faker.company() + ' ' + random.choice(['Delegacia', 'Departamento', 'Central'])
            Delegacia.objects.create(
                nome=nome[:200],
                tipo=random.choice(tipos),
                cidade='Palmas — TO',
                endereco=faker.street_address(),
                telefone=faker.phone_number(),
                horario=f'{random.randint(8, 10)}h às {random.randint(17, 20)}h',
                url='https://www.example.com',
                ativo=random.choice([True, True, False]),
            )
        self.stdout.write(f'  Delegacias adicionadas: {count}')

    def _create_videos(self, faker, count):
        sample_urls = [
            'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'https://www.youtube.com/watch?v=3JZ_D3ELwOQ',
            'https://www.youtube.com/watch?v=2Vv-BfVoq4g',
            'https://www.youtube.com/watch?v=LHCob76kigA',
            'https://www.youtube.com/watch?v=ZbZSe6N_BXs',
        ]
        for _ in range(count):
            Video.objects.create(
                titulo=faker.sentence(nb_words=6)[:200],
                descricao=faker.paragraph(nb_sentences=3),
                url_youtube=random.choice(sample_urls),
            )
        self.stdout.write(f'  Vídeos adicionados: {count}')

    def _create_denuncias(self, User, faker, count):
        tipos = [choice[0] for choice in Denuncia.TIPOS_GOLPE]
        faixas = [choice[0] for choice in Denuncia.FAIXAS_ETARIAS]
        statuses = [choice[0] for choice in Denuncia.STATUS_DENUNCIA]

        usuarios = list(User.objects.filter(tipo_usuario='usuario'))
        moderadores = list(User.objects.filter(tipo_usuario='moderador'))

        for _ in range(count):
            anonima = random.choice([True, False, False])
            usuario = None if anonima else random.choice(usuarios) if usuarios else None
            tipo_golpe = random.choice(tipos)
            faixa_etaria = random.choice(faixas)
            data_ocorrencia = faker.date_between(start_date='-1y', end_date='today')
            cidade = 'Palmas — TO'
            descricao = faker.paragraph(nb_sentences=5)
            status = random.choice(statuses)
            publicada = status == 'aprovada'
            moderado_por = random.choice(moderadores) if status != 'analise' and moderadores else None
            moderado_em = timezone.now() if moderado_por else None
            motivo_moderacao = faker.sentence(nb_words=10) if status != 'analise' else ''
            publicada_em = timezone.now() if publicada else None

            denuncia = Denuncia(
                anonima=anonima,
                usuario=usuario,
                tipo_golpe=tipo_golpe,
                faixa_etaria=faixa_etaria,
                data_ocorrencia=data_ocorrencia,
                cidade=cidade,
                descricao=descricao,
                status=status,
                moderado_por=moderado_por,
                moderado_em=moderado_em,
                motivo_moderacao=motivo_moderacao,
                publicada=publicada,
                publicada_em=publicada_em,
            )
            denuncia.save()

        self.stdout.write(f'  Denúncias criadas: {count}')

    def _generate_cpf(self):
        digits = [random.randint(0, 9) for _ in range(11)]
        return '{}.{}.{}-{}'.format(
            ''.join(str(d) for d in digits[:3]),
            ''.join(str(d) for d in digits[3:6]),
            ''.join(str(d) for d in digits[6:9]),
            ''.join(str(d) for d in digits[9:11]),
        )
