from django.db import migrations
from django.contrib.auth.hashers import make_password

def criar_usuarios(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    senha_hash = make_password('ifto2026')

    if not User.objects.filter(username='admin').exists():
        User.objects.create(
            username='admin', email='admin@sistema.local', password=senha_hash,
            is_superuser=True, is_staff=True, is_active=True,
            nome_completo='Aldemir Nistrador de Sousa', tipo_usuario='admin'
        )

    if not User.objects.filter(username='moderador').exists():
        User.objects.create(
            username='moderador', email='mod@sistema.local', password=senha_hash,
            is_superuser=False, is_staff=False, is_active=True,
            nome_completo='Moderaderson da Silva', tipo_usuario='moderador'
        )

    if not User.objects.filter(username='usuario').exists():
        User.objects.create(
            username='usuario', email='user@sistema.local', password=senha_hash,
            is_superuser=False, is_staff=False, is_active=True,
            nome_completo='Fulano de Tal', tipo_usuario='usuario'
        )

def remover_usuarios(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    User.objects.filter(username__in=['admin', 'moderador', 'usuario']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(criar_usuarios, reverse_code=remover_usuarios),
    ]