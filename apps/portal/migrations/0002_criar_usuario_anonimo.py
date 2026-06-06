from django.db import migrations


# ─── Dados fixos do usuário técnico anônimo ───────────────────────────────────
# Estes valores NÃO devem ser alterados após o deploy em produção.
# O username é referenciado em settings.ANONYMOUS_COMPLAINT_USERNAME.
ANONIMO_USERNAME = 'anonimo_sistema'
ANONIMO_EMAIL = 'anonimo@sistema.local'
ANONIMO_FIRST_NAME = 'Usuário'
ANONIMO_LAST_NAME = 'Anônimo'


def criar_usuario_anonimo(apps, schema_editor):
    """
    Cria o usuário técnico fixo para denúncias anônimas.

    Características de segurança:
        - is_active=False  → não consegue fazer login pela tela de auth
        - set_unusable_password() → senha inutilizável, nunca autentica
        - is_staff=False   → sem acesso ao admin
        - is_superuser=False → sem permissões especiais
        - Criado com get_or_create → idempotente (pode rodar várias vezes)
    """
    User = apps.get_model('accounts', 'User')

    usuario, criado = User.objects.get_or_create(
        username=ANONIMO_USERNAME,
        defaults={
            'email': ANONIMO_EMAIL,
            'first_name': ANONIMO_FIRST_NAME,
            'last_name': ANONIMO_LAST_NAME,
            'is_active': False,       # não pode fazer login
            'is_staff': False,        # sem acesso ao admin
            'is_superuser': False,    # sem permissões especiais
        }
    )

    if criado:
        # Senha inutilizável — impossível autenticar mesmo com força bruta
        usuario.set_unusable_password()
        usuario.save()


def remover_usuario_anonimo(apps, schema_editor):
    """
    Rollback: remove o usuário técnico SE não houver denúncias vinculadas.

    Se já existirem denúncias, a remoção falha silenciosamente para
    preservar integridade referencial (FK com PROTECT no model).
    """
    User = apps.get_model('accounts', 'User')
    Denuncia = apps.get_model('portal', 'Denuncia')

    try:
        usuario = User.objects.get(username=ANONIMO_USERNAME)
        if not Denuncia.objects.filter(usuario=usuario).exists():
            usuario.delete()
    except User.DoesNotExist:
        pass  # Já não existe, nada a fazer


class Migration(migrations.Migration):
    """
    Data migration que insere o usuário técnico anônimo no banco.

    Este usuário é o destino de TODAS as denúncias marcadas como anônimas.
    Nenhuma consulta SQL, log ou relatório conseguirá vincular uma denúncia
    anônima ao usuário real — o FK sempre apontará para este registro técnico.

    Dependência: precisa que a tabela portal_denuncia já exista (0001).
    """

    dependencies = [
        ('portal', '0001_denuncia_model'),
    ]

    operations = [
        migrations.RunPython(
            criar_usuario_anonimo,
            reverse_code=remover_usuario_anonimo,
        ),
    ]
