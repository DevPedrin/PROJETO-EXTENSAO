from pathlib import Path
from decouple import config, Csv
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Modo de execução ─────────────────────────────────────────────────────────
# USE_SQLITE=True  → banco local SQLite (desenvolvimento, sem PostgreSQL)
# USE_SQLITE=False → banco PostgreSQL (produção / Docker)
USE_SQLITE = config('USE_SQLITE', default=True, cast=bool)

SECRET_KEY = config('SECRET_KEY', default='chave-local-insegura-apenas-para-dev')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# ─── Validação de variáveis obrigatórias apenas em modo PostgreSQL ─────────────
if not USE_SQLITE:
    from decouple import UndefinedValueError
    REQUIRED_VARS = ["SECRET_KEY", "POSTGRES_DB", "POSTGRES_USER", "POSTGRES_PASSWORD", "DB_HOST"]
    for var in REQUIRED_VARS:
        try:
            config(var)
        except UndefinedValueError:
            raise Exception(f"Variável obrigatória não definida no .env: {var}")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.portal',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Banco de Dados ───────────────────────────────────────────────────────────
# Chaveado pela variável USE_SQLITE do .env
# USE_SQLITE=True  → SQLite local (padrão para desenvolvimento)
# USE_SQLITE=False → PostgreSQL (produção / Docker)

if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('POSTGRES_DB'),
            'USER': config('POSTGRES_USER'),
            'PASSWORD': config('POSTGRES_PASSWORD'),
            'HOST': config('DB_HOST'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Araguaina'

USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'accounts.User'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

# ─── Anonimato de denúncias ───────────────────────────────────────────────────
# Username do usuário técnico fixo para denúncias anônimas.
# Esse usuário é criado automaticamente via data migration (0002).
# Nunca altere este valor após o banco ser populado em produção.
ANONYMOUS_COMPLAINT_USERNAME = 'anonimo_sistema'