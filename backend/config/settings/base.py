import dj_database_url
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parents[4]  # .../justintime-platform
BACKEND_DIR = BASE_DIR / "justintime-platform" / "backend"

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DJANGO_DEBUG", "0") == "1"

ALLOWED_HOSTS = [h.strip() for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Domain apps
    "apps.accounts.apps.AccountsConfig",
    "apps.core",
    "apps.leads",
    "apps.recruitment",
    "apps.training",
    "apps.blog",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "DIRS": [BACKEND_DIR / "templates"],
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.core.context_processors.newsletter_form",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL", ""),
        conn_max_age=60,
    )
}

AUTH_USER_MODEL = "accounts.User"

# Static & media
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BACKEND_DIR / "static",
]
STATIC_ROOT = os.environ.get("STATIC_ROOT", str(BASE_DIR / "staticfiles"))

MEDIA_URL = "/media/"
MEDIA_ROOT = os.environ.get("MEDIA_ROOT", str(BASE_DIR / "media"))

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Basic logging (expanded later)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/portal/"
LOGOUT_REDIRECT_URL = "/"

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "no-reply@justintime.local",
)

RECRUITMENT_NOTIFY_EMAIL = os.environ.get(
    "RECRUITMENT_NOTIFY_EMAIL",
    "hr@justintime.local",
)

TRAINING_NOTIFY_EMAIL = os.environ.get(
    "TRAINING_NOTIFY_EMAIL", 
    "training@justintime.local",
)

LEADS_NOTIFY_EMAIL = os.environ.get(
    "LEADS_NOTIFY_EMAIL", 
    "leads@justintime.local"
)

CONTACT_NOTIFY_EMAIL = os.environ.get(
    "CONTACT_NOTIFY_EMAIL", 
    "contact@justintime.local"
)