"""
Django settings for My_Market project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--5m5ng0gi_##p-um4m1e0!46&pd&^)y+6d)f^k%u17dl2kn9=7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'sorl.thumbnail',
    'django_filters',

    'core',
    'product',
    'customer',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'core.middleware.TimeMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'My_Market.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.my_contexts',
            ],
        },
    },
]

WSGI_APPLICATION = 'My_Market.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'my_market',
        'USER': 'postgres',
        'PASSWORD': 'am14201378',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en-us', 'English'),
    ('fa', 'Persian'),
)

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'media',
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOCALE_PATHS = [BASE_DIR / 'locale']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

AUTH_USER_MODEL = 'core.User'

from logging import LogRecord


def length_limit(record: LogRecord) -> bool:
    return len(record.getMessage()) > 20


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'short': {
            'format': '{levelname} : {asctime} {message}',
            'style': '{',
        },
        'verbose': {
            'format': '{levelname}: {message} at {module} (process: {process}, thread: {thread})',
            'style': '{',
        },
    },
    'filters': {
        'length_limit': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': length_limit,
        },
    },
    'handlers': {
        'my-console': {
            'class': 'logging.StreamHandler',
            'formatter': 'short',
            'filters': ['length_limit'],
        },
        'my-file': {
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'log/my-log.log',
        },
    },
    'root': {
        'handlers': ['my-console'],
        'level': 'DEBUG'
    },
    'loggers': {
        'project': {
            'handlers': ['my-file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'project.developers': {
            'handlers': ['my-console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}
from django.urls import reverse_lazy
LOGIN_URL = reverse_lazy('customer:customer_login')
# LOGIN_REDIRECT_URL = '/customer/profile/'
LOGIN_REDIRECT_URL = reverse_lazy('home')

CKEDITOR_UPLOAD_PATH = 'ck/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
TAGGIT_CASE_INSENSITIVE = True
