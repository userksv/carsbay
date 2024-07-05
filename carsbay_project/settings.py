from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

ENV = os.environ.get('ENV')
if ENV == 'dev':
   DEBUG = True
else: 
    DEBUG = False

ALLOWED_HOSTS = ['*']

if not DEBUG:
    # uncomment in production
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(' ')
    # ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django_extensions",
    "crispy_forms",
    "crispy_bootstrap5",
    "sorl.thumbnail",
    "widget_tweaks",
    "users.apps.UsersConfig",
    "main.apps.MainConfig",
    "chat.apps.ChatConfig",
    "news.apps.NewsConfig",
    "search.apps.SearchConfig",
    "django.contrib.humanize",
    "rest_framework",
    'storages',
    'rosetta',
    # 'djmoney',
    #########################
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]


# Channels
REDIS_URL = os.environ['REDIS_URL']

if DEBUG == True:
    REDIS_URL = 'redis://localhost:6379'

ASGI_APPLICATION = "carsbay_project.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_URL)],
        },
    },
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",    
]

ROOT_URLCONF = "carsbay_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "carsbay_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if ENV == 'dev':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": 
        {
            "ENGINE":   "django.db.backends.postgresql_psycopg2",
            "NAME":     os.environ['DB_NAME'],
            "USER":     os.environ['DB_USER'],
            "PASSWORD": os.environ['DB_PASS'],
            "HOST":     os.environ['DB_HOST'],
            "PORT":     os.environ['DB_PORT'],
        }
    }

AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
DEFAULT_FILE_STORAGE = 'storages.backends.s3.S3Storage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / 'media'

STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_URL = "/staticfiles/"
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en"

TIME_ZONE = os.getenv('TIME_ZONE')

USE_I18N = True

USE_TZ = True

LANGUAGES = (
    ('en', 'English'),
    ('ru', 'Russian')
)

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

#########
CRISPY_TEMPLATE_PACK = "bootstrap5"
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

LOGIN_REDIRECT_URL = "home"
LOGIN_URL = "login"

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv('SERVER_HOST')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('SERVER_EMAIL')
EMAIL_HOST_PASSWORD = os.getenv('SERVER_EMAIL_PASS')

# for smart-selects extension
# JQUERY_URL = True
USE_DJANGO_JQUERY = True

# convert datatime object to int
REST_FRAMEWORK = {
    'DATETIME_FORMAT': '%s000',
}

if not DEBUG:
    # Uncomment in production!!!
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
#     SECURE_HSTS_SECONDS = 3600
#     SECURE_SSL_REDIRECT = True
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SECURE_HSTS_INCLUDE_SUBDOMAINS=True
#     SECURE_HSTS_PRELOAD=True

CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS').split(' ')

