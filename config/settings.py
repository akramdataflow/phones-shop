from django.utils.translation import gettext_lazy as _
from django.contrib.messages import constants as message_constants
from pathlib import Path
import os
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', default="django-insecure--bqof15wiq1h2wl4+$j*soajbbj#zoalpeto0nwju&42ng$ftr")

#DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() == "true"
DEBUG = True

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", default="*").split(",")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'easy_thumbnails',

    'core',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.site_common',
            ],
        },
    },
]

LOGIN_URL = '/login/'

LOGOUT_REDIRECT_URL = '/'

ASGI_APPLICATION = "config.asgi.application"

WSGI_APPLICATION = 'config.wsgi.application'

DATABASE_PROD = os.environ.get("DATABASE_PROD", default="0") == "1"

DATABASES = {
    "default": {
        'OPTIONS': {
            'options': '-c search_path=public'
        },
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get('DATABASE_NAME', default='mustafa'),
        "USER": os.environ.get('DATABASE_USER', default='mustafa'),
        "PASSWORD": os.environ.get('DATABASE_PASSWORD', default='top_secret'),
        "HOST": os.environ.get('DATABASE_HOST', default='127.0.0.1'),
        "PORT": os.environ.get('DATABASE_PORT', default=5432),
    } if DATABASE_PROD else {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True

LANGUAGES = [
    ('en', _('English')),
    ('ar', _('Arabic')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR/'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

MESSAGE_TAGS = {
    message_constants.DEBUG: 'info',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}

SITE_TITLE = "Store site admin"

SITE_HEADER = "Store administration"

INDEX_TITLE = "Dashboard administration"

SESSION_COOKIE_SECURE = os.environ.get("SESSION_COOKIE_SECURE", default="0") == "1"
CSRF_COOKIE_SECURE = os.environ.get("CSRF_COOKIE_SECURE", default="0") == "1"

CSRF_TRUSTED_ORIGINS = os.environ.get("CSRF_TRUSTED_ORIGINS", default="http://127.0.0.1").split(',')
CSRF_ALLOWED_ORIGINS = os.environ.get("CSRF_ALLOWED_ORIGINS", default="").split(',')
CORS_ORIGINS_WHITELIST = os.environ.get("CORS_ORIGINS_WHITELIST", default="").split(',')

AUTHENTICATION_BACKENDS = [
    'main.backends.PhoneEmailUsernameBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

THUMBNAIL_ALIASES = {
    '': {
        'product': {'size': (270, 270), 'crop': True},
    },
}