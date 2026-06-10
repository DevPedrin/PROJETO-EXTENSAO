import hashlib
import hmac
from django.conf import settings


def gerar_hash_usuario(user):
    return hmac.new(
        settings.SECRET_KEY.encode(),
        str(user.pk).encode(),
        hashlib.sha256
    ).hexdigest()