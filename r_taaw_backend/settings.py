import os
import sys
from pathlib import Path

from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = "/tmp/logs"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1",
    "http://localhost",
    "http://r-taaw.allworld.xyz:80",
]
extra_origins = config("CORS_ALLOWED", default="", cast=str)
if extra_origins:
    CORS_ALLOWED_ORIGINS += [origin.strip() for origin in extra_origins.split(",") if origin.strip()]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_extensions",
    "rest_framework",
    "drf_spectacular",
    "cookbook",
    "users",
]

BASE_MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "middlewares.localization.NormalizingLocaleMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

MIDDLEWARE = (
    [
        "middlewares.log_all_requests.LogAllRequestsMiddleware",
    ]
    + BASE_MIDDLEWARE
    if DEBUG
    else BASE_MIDDLEWARE
)

ROOT_URLCONF = "r_taaw_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "r_taaw_backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "R‑Taaw: Recipes to Remember API",
    "DESCRIPTION": "API for managing recipes, ingredients and users",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname:<8} {name:<20} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "verbose",
        },
        "file": {
            "level": "DEBUG" if DEBUG else "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(LOG_DIR, "django.log"),
            "maxBytes": 1024 * 1024 * 100,  # 100 MB
            "backupCount": 5,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django.server": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "users": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG" if DEBUG else "INFO",
        },
    },
}

LANGUAGE_CODE = "en"
LANGUAGES = [
    ("sq", "Albanian - Shqip"),
    ("ar", "Arabic - عربي"),
    ("az", "Azerbaijani - Azərbaycan"),
    ("eu", "Basque - Euskara"),
    ("bn", "Bengali - বাংলা"),
    ("bg", "Bulgarian - Български"),
    ("ca", "Catalan - Català"),
    ("zh-hans", "Chinese (Simplified) - 中文"),
    ("zh-hant", "Chinese (Traditional) - 繁體中文"),
    ("hr", "Croatian - Hrvatski"),
    ("cs", "Czech - Čeština"),
    ("da", "Danish - Dansk"),
    ("nl", "Dutch - Nederlands"),
    ("en", "English"),
    ("eo", "Esperanto - Esperanto"),
    ("et", "Estonian - Eesti"),
    ("fi", "Finnish - Suomi"),
    ("fr", "French - Français"),
    ("gl", "Galician - Galego"),
    ("de", "German - Deutsch"),
    ("el", "Greek - Ελληνικά"),
    ("he", "Hebrew - עברית"),
    ("hi", "Hindi - हिन्दी"),
    ("hu", "Hungarian - Magyar"),
    ("is", "Icelandic - Íslenska"),
    ("id", "Indonesian - Bahasa Indonesia"),
    ("ga", "Irish - Gaeilge"),
    ("it", "Italian - Italiano"),
    ("ja", "Japanese - 日本語"),
    ("ko", "Korean - 한국어"),
    ("lv", "Latvian - Latviešu"),
    ("lt", "Lithuanian - Lietuvių"),
    ("ms", "Malay - Bahasa Melayu"),
    ("nb", "Norwegian - Norsk Bokmål"),
    ("fa", "Persian - فارسی"),
    ("pl", "Polish - Polski"),
    ("pt", "Portuguese - Português"),
    ("pt-br", "Portuguese (Brazil) - Português (Brasil)"),
    ("ro", "Romanian - Română"),
    ("ru", "Russian - Русский"),
    ("sk", "Slovak - Slovenčina"),
    ("sl", "Slovenian - Slovenščina"),
    ("es", "Spanish - Español"),
    ("sv", "Swedish - Svenska"),
    ("tl", "Tagalog - Tagalog"),
    ("th", "Thai - ไทย"),
    ("tr", "Turkish - Türkçe"),
    ("uk", "Ukrainian - Українська"),
    ("ur", "Urdu - اردو"),
]

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [
    BASE_DIR / "locale",
]

AUTH_USER_MODEL = "users.UserModel"

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "files", "media")
STATIC_ROOT = os.path.join(BASE_DIR, "static")

ADMIN_EMAIL = config("ADMIN_EMAIL")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

TESTING = any("test" in arg for arg in sys.argv)

if DEBUG:
    if TESTING:
        EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
    else:
        EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
        EMAIL_FILE_PATH = os.path.join(LOG_DIR, "django_emails.log")

else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = config("EMAIL_HOST")
    EMAIL_PORT = config("EMAIL_PORT", cast=int)
    EMAIL_HOST_USER = config("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
    DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

SHELL_PLUS_PRINT_SQL_TRUNCATE = None
