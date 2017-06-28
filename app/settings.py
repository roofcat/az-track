# -*- coding: utf-8 -*-


"""
Django settings for app project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""


from __future__ import absolute_import


import os
import sys


reload(sys)
sys.setdefaultencoding('utf-8')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ef-d+%grya6#*xrn+fztnsh1-lz2%8c@t!o3clkhp@gfx%7p(-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # app de terceros
    'django_celery_beat',
    'rest_framework',
    'rest_framework.authtoken',
    'storages',
    # apps
    'autenticacion',
    'configuraciones',
    'customsearch',
    'dashboard',
    'emails',
    'empresas',
    'perfiles',
    'reports',
    'resumen',
    'tipodocumentos',
    'webhooks',
]

REST_FRAMEWORK = {
    'PAGE_SIZE': 50,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'track',
        'USER': 'root',
        'PASSWORD': '12345',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'es-CL'

TIME_ZONE = 'America/Santiago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

if DEBUG:
    STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'


# Configuración de google cloud storage
DEFAULT_FILE_STORAGE = 'storages.backends.gs.GSBotoStorage'
GS_ACCESS_KEY_ID = 'GOOG3EVOJB54TQ5XPNZK'
GS_SECRET_ACCESS_KEY = '1LmcAXenaUGNwRQ7fL6gJACjqJI/PYUIf7rD5ptu'
GS_BUCKET_NAME = 'folkloric-light-prueba'


# definir la url para obtener los archivos adjuntos
MEDIA_URL = 'https://storage.googleapis.com/'
MEDIA_ROOT = 'https://storage.googleapis.com/'


# Configuración de archivos de logs
LOGGING_BACKUP_COUNT = 10
LOGGING_LEVEL = 'DEBUG' if DEBUG else 'INFO'
LOGGING_WHEN = 'D'
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d] \n %(message)s \n \n",
        },
        "simple": {
            "format": "[%(levelname)s] \n %(message)s",
        },
    },
    "handlers": {
        "autenticacion_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/autenticacion.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "configuraciones_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/configuraciones.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "customsearch_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/customsearch.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "dashboard_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/dashboard.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "emails_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/emails.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "empresas_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/empresas.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "perfiles_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/perfiles.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "reports_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/reports.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "resumen_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/resumen.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "tipodocumentos_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/tipo_documentos.log",
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "utils_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/utils.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "webhooks_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/webhooks.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "django_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/django.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
        "utils_file": {
            "level": LOGGING_LEVEL,
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/utils.log",
            "backupCount": LOGGING_BACKUP_COUNT,
            "when": LOGGING_WHEN,
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["django_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "autenticacion": {
            "handlers": ["autenticacion_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "configuraciones": {
            "handlers": ["configuraciones_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "customsearch": {
            "handlers": ["customsearch_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "dashboard": {
            "handlers": ["dashboard_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "emails": {
            "handlers": ["emails_file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "empresas": {
            "handlers": ["empresas_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "perfiles": {
            "handlers": ["perfiles_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "reports": {
            "handlers": ["reports_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "resumen": {
            "handlers": ["resumen_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "tipodocumentos": {
            "handlers": ["tipodocumentos_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "utils": {
            "handlers": ["utils_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "webhooks": {
            "handlers": ["webhooks_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
        "utils": {
            "handlers": ["utils_file"],
            "level": LOGGING_LEVEL,
            "propagate": True,
        },
    },
}
