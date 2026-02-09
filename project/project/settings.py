from pathlib import Path
import os
from dotenv import load_dotenv


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent


def val_u(key: str):
    val = os.getenv(key)
    if val is None:
        return ''
    return val


print(
        val_u('DJANGO_DEBUG'),
        val_u('DJANGO_ALLOWED_HOSTS'),
        val_u('DJANGO_SECRET_KEY'),
        val_u('DJANGO_DATABASE_ENGINE'),
        val_u('DJANGO_DATABASE_NAME'),
      )

DEBUG = val_u('DJANGO_DEBUG')
ALLOWED_HOSTS = [val_u('DJANGO_ALLOWED_HOSTS')]
SECRET_KEY = val_u('DJANGO_SECRET_KEY')
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': val_u('DJANGO_DATABASE_ENGINE'),
            'NAME': BASE_DIR / val_u('DJANGO_DATABASE_NAME'),
        }
    }

WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
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
    'user',
    'models',
    'details',
    'mailbox',
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

# settings.py
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/dashboard/"
LOGOUT_REDIRECT_URL = "/login/"
