"""
Django settings for webtrition project.

Generated by 'django-admin startproject' using Django 2.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import environ
import re
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = environ.Path(__file__) - 3
PROJECT_DIR = BASE_DIR.path("project")

env = environ.Env()
# environ.Env.read_env(str(BASE_DIR.path('.env')))


def get_version():
    """
    Return package version as listed in `__version__` in `init.py`.
    """
    init_py = open(os.path.join(BASE_DIR, "__init__.py")).read()
    return re.match("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


VERSION = get_version()


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

ADMINS = [("Alex", "alex@doubledash.io"), ("Mathieu", "mathieu@doubledash.io")]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # 3rd party
    "bootstrap4",
    "crispy_forms",
    "django_q",
    "storages",
    # Apps
    "ops",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "config.middlewares.CurrentVersionMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            str(BASE_DIR.path("templates")),
        ],
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

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL"),
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Montreal"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Cache
# ------------------------------------------------------------------------------
REDIS_URL = env("REDIS_URL", default="redis://redis:6379")
REDIS_LOCATION = "{0}/{1}".format(REDIS_URL, env("REDIS_DB", default=0))

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_LOCATION,
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"

# Auth Configuration
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "login"

# Logging Configuration
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "django": {
            "level": "INFO",
        },
        "boto3": {
            "level": "CRITICAL",
        },
        "botocore": {
            "level": "CRITICAL",
        },
        "s3transfer": {
            "level": "CRITICAL",
        },
        "requests": {
            "level": "WARNING",
        },
        "urllib3": {
            "level": "WARNING",
        },
        "slack_bolt": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

# django-q
# ------------------------------------------------------------------------------
Q_CLUSTER = {
    "cpu_affinity": 1,
    "django_redis": "default",
    "label": "Django Q",
    "name": "ops_status",
    "retry": 60,
    "timeout": 30,
}

# django-storages
# ------------------------------------------------------------------------------
MEDIA_URL = "/media/"
MEDIA_ROOT = str(BASE_DIR.path("media"))
DEFAULT_FILE_STORAGE = "config.storages.MediaRootFileSystemStorage"

STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR.path("static"))

STATICFILES_DIRS = [str(PROJECT_DIR.path("static"))]

# django-crispy-forms
# ------------------------------------------------------------------------------
CRISPY_TEMPLATE_PACK = "bootstrap4"

# Slack
# ------------------------------------------------------------------------------
SLACK_CLIENT_ID = env("SLACK_CLIENT_ID")
SLACK_CLIENT_SECRET = env("SLACK_CLIENT_SECRET")
SLACK_SIGNING_SECRET = env("SLACK_SIGNING_SECRET")
SLACK_SCOPES = env("SLACK_SCOPES")
