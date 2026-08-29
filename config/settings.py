"""Settings for the DjangoSIGE project."""

from pathlib import Path

from decouple import Csv, config
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).resolve().parent.parent
APPS_DIR = BASE_DIR / "djangosige"

# Geral
# -----
DEBUG = config("DEBUG", cast=bool)
SECRET_KEY = config("SECRET_KEY")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

TIME_ZONE = "America/Sao_Paulo"
LANGUAGE_CODE = "pt-br"
USE_I18N = True
USE_TZ = True

# Banco de Dados
# --------------
DATABASES = {"default": config("DATABASE_URL", cast=db_url)}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cache
# -----
CACHES = {
    "default": {
        "BACKEND": (
            "django.core.cache.backends.locmem.LocMemCache" if DEBUG else "django.core.cache.backends.redis.RedisCache"
        ),
        "LOCATION": "" if DEBUG else config("REDIS_URL"),
    }
}

# URLs
# ----
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Apps
# ----
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "crispy_forms",
    "crispy_bootstrap5",
    "djangosige",
    "djangosige.accounts",
    "djangosige.cadastros",
    "djangosige.apps.base",
    "djangosige.apps.login",
    "djangosige.apps.cadastro",
    "djangosige.apps.vendas",
    "djangosige.apps.compras",
    "djangosige.apps.fiscal",
    "djangosige.apps.financeiro",
    "djangosige.apps.estoque",
]

if DEBUG:
    INSTALLED_APPS += [
        "debug_toolbar",
        "django_extensions",
    ]

# Middleware
# ----------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if DEBUG:
    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

# Autenticação
# -------------
AUTH_USER_MODEL = "auth.User"
LOGIN_REDIRECT_URL = "pagina_inicial"
LOGIN_URL = "accounts:login"
LOGOUT_REDIRECT_URL = "accounts:login"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Arquivos estáticos
# ------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    str(BASE_DIR / "node_modules"),
]

# Arquivos de mídia
# -----------------
MEDIA_URL = "/media/"
MEDIA_ROOT = APPS_DIR / "media"

# Templates
# ---------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "djangosige.apps.base.context_version.sige_version",
                "djangosige.apps.login.context_user.foto_usuario",
            ],
        },
    },
]

# Crispy Forms
# -------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Fixtures
# --------
FIXTURE_DIRS: list[str] = []

# Email
# -----
DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)
EMAIL_HOST_USER = config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

if DEBUG:
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS": [
            "debug_toolbar.panels.redirects.RedirectsPanel",
            # Disable profiling panel due to an issue with Python 3.12+:
            # https://github.com/jazzband/django-debug-toolbar/issues/1875
            "debug_toolbar.panels.profiling.ProfilingPanel",
        ],
        "SHOW_TEMPLATE_CONTEXT": True,
    }
    INTERNAL_IPS = ["127.0.0.1", "10.0.2.2"]
    SITE_ID = 1
