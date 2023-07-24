from pathlib import Path
from django.contrib.messages import constants as messages
from whitenoise.storage import CompressedManifestStaticFilesStorage
import django_heroku, dj_database_url, os


BASE_DIR = Path(__file__).resolve().parent.parent

class WhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

SECRET_KEY = 'django-insecure-u)v29=70rm^79^_$p-63f9-35i=pumaoegwaf#*bi+-#v=^&bj'

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = ['*']
INTERNAL_IPS = [
    "127.0.0.1",
]

X_FRAME_OPTIONS = 'SAMEORIGIN'
XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'stock_app',
    'crispy_forms',
    'django_celery_beat',
    'django.contrib.humanize'
]

BROKER_CONNECTION_RETRY = True
BROKER_CONNECTION_MAX_RETRIES = 0

MESSAGE_TAGS = {
        messages.DEBUG: 'alert-secondary',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
 }

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'stock.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'stock_screener_db_production',
        'USER': 'postgres',
        'PASSWORD': 'mwhorse',
        'HOST': 'localhost',
        'PORT':'5432'
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd5eqnfr8rpafjt',
        'USER': 'u8f9qadujk81ii',
        'PASSWORD': 'p4f52eaa5dcbdc1f5d9cb444e0771129d4f2fdf84a62b5b248765fe4bd2a3e3d2',
        'HOST': 'ec2-3-209-94-155.compute-1.amazonaws.com',
        'PORT':'5432'
    }
}
'''
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files
STATIC_URL = '/static/'
if DEBUG:
        STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static')
       ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_STORAGE = '.storage.WhiteNoiseStaticFilesStorage'
django_heroku.settings(locals())

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT= 587
EMAIL_HOST_USER = "stefan.programming22@gmail.com"
EMAIL_HOST_PASSWORD = "fysfiprafzzsijqs"

# Celery rabbitmq config
CELERY_BROKER_URL = 'amqps://dtbbvvno:u6feZKHbrux8fSObOw1Sg7c34KAWExki@woodpecker.rmq.cloudamqp.com/dtbbvvno'
BROKER_URL = 'amqps://dtbbvvno:u6feZKHbrux8fSObOw1Sg7c34KAWExki@woodpecker.rmq.cloudamqp.com/dtbbvvno'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = False # set to true