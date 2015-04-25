"""
Django settings for kontent project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# This directory can be overridden by a custom theme
#TEMPLATE_DIR = BASE_DIR + '/kontent/templates/'
TEMPLATE_DIRS = (os.path.join(BASE_DIR, '/kontent/templates/'), )


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ahgm0u*eh@lb0wvqtyle0x0glh3&dx-&0---#yy!q0j%x#*9(#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django.contrib.sites',
    'django.contrib.redirects',
    'markdown_deux',
    'kontent',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.redirects.middleware.RedirectFallbackMiddleware',
)

ROOT_URLCONF = 'kontentsite.urls'

WSGI_APPLICATION = 'kontentsite.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
#STATIC_ROOT = os.path.join(BASE_DIR, 'static', '')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    '/var/www/static/',
)


# Default to the first site of the Django sites. Overrule in local_settings.py
SITE_ID = 1

# Hashids salt
HASHIDS_SALT = 'overwrite with a real salt'

# Custom settings for this (dev) environment
try:
    from local_settings import *
except ImportError:
    pass

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_DATABASE,
        'USER': DB_USERNAME,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOSTNAME,
        'PORT': '',
    },
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #}
}


from markdown_deux.conf.settings import MARKDOWN_DEUX_DEFAULT_STYLE

MARKDOWN_DEUX_STYLES = {
    "default": MARKDOWN_DEUX_DEFAULT_STYLE,
    "normal": {
        "extras": {
            "code-friendly": None,
        },
        # Allow raw HTML (WARNING: don't use this for user-generated
        # Markdown for your site!).
        "safe_mode": False,
    }
}
