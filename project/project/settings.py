from pathlib import Path
import os
from dotenv import load_dotenv


_ = load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


def val_u(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        return ''
    return val


DEBUG = val_u('DJANGO_DEBUG') != 'False'
ALLOWED_HOSTS = val_u('DJANGO_ALLOWED_HOSTS').split(',')
SITE_URL = val_u('SITE_URL')
SECRET_KEY = val_u('DJANGO_SECRET_KEY')
DATABASES = {
    'default': {
        'ENGINE': val_u('DJANGO_DATABASE_ENGINE'),
        'NAME': BASE_DIR / val_u('DJANGO_DATABASE_NAME'),
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DATE_FORMAT = "m-d-y" 

STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
ASSET_URL = '/assets/'
ASSET_ROOT = BASE_DIR / 'assets'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
    'base',
    'explore',
    'host',
    'invoice',
    'share',
    'mailbox',
    'models',
    'play',
    'user',

]


ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'project' / 'templates',
            ],
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

__DCAPV = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': __DCAPV + '.UserAttributeSimilarityValidator'},
    {'NAME': __DCAPV + '.MinimumLengthValidator'},
    {'NAME': __DCAPV + '.CommonPasswordValidator'},
    {'NAME': __DCAPV + '.NumericPasswordValidator'},
]

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/'

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

ENABLE_EMAIL_NOTIFICATIONS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'apikey'
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_API_KEY')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format": (
                "[%(log_color)s%(levelname)-8s%(reset)s] "
                "%(blue)s%(name)s:%(lineno)-4d%(reset)s "
                "%(white)s%(message)s%(reset)s "
                ),
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "colored",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}
