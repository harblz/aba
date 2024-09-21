"""
Django settings for abarocks project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

from pathlib import Path
import os
import tempfile
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False) == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(":")
INTERNAL_IPS = ALLOWED_HOSTS

MANAGERS = [("Alex", "harblz@gmail.com"), ("Kyle", "kyle@nullandvoid.digital")]
ADMINS = [("Alex", "harblz@gmail.com"), ("Kyle", "kyle@nullandvoid.digital")]

SERVER_EMAIL = "noreply@behaviorist.tech"  # TODO: Update email address

# Google Analytics
GOOGLE_ANALYTICS_PROPERTY_ID = "UA-98470698-1"
GOOGLE_ANALYTICS_DOMAIN = "aba.rocks"

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",  # Use Whitenoise w/ `manage.py runserver`
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "taggit",
    "ckeditor",
    "django_htmx",
    "django_bootstrap5",
    "fontawesomefree",
    "polls.apps.PollsConfig",
    "quiz.apps.QuizConfig",
    "blog.apps.BlogConfig",
    "fluency.apps.FluencyConfig",
    "learn.apps.LearnConfig",
    "pages.apps.PagesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

# Debug Toolbar and Extensions only when `DEBUG = False` and not running tests
ENABLE_DEBUG_TOOLBAR = DEBUG and "test" not in sys.argv
if ENABLE_DEBUG_TOOLBAR:
    INSTALLED_APPS += [
        "django_extensions",
        "debug_toolbar",
    ]
    MIDDLEWARE[:0] = [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
    DEBUG_TOOLBAR_CONFIG = {"ROOT_TAG_EXTRA_ATTRS": "hx-preserve"}

ROOT_URLCONF = "abarocks.urls"

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

WSGI_APPLICATION = "abarocks.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "data/db.sqlite3",
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(tempfile.gettempdir(), "ck_media")

# Whitenoise compression & caching
# https://whitenoise.readthedocs.io/en/latest/django.html
"""STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}"""

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Stripe
# https://docs.stripe.com/api?lang=python
STRIPE_PUBLISHABLE_KEY = os.environ.get("STRIPE_PUBLISHABLE_KEY")
STRIPE_SECRET_KEY = os.environ.get("STRIPE_SECRET_KEY")

# CKEditor
# https://django-ckeditor.readthedocs.io/en/latest/
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_CONFIGS = {
    "default": {
        "width": "100%",
        "toolbar": "Custom",
        "toolbar_Custom": [
            [
                "Styles",
                "Format",
                "Templates",
                "CopyFormatting",
                "RemoveFormat",
                "PageBreak",
            ],
            ["Image", "Table", "HorizontalRule", "SpecialChar"],
            [
                "NumberedList",
                "BulletedList",
                "-",
                "Outdent",
                "Indent",
                "-",
                "Blockquote",
                "JustifyLeft",
                "JustifyCenter",
                "JustifyRight",
                "JustifyBlock",
            ],
            ["Link", "Unlink"],
            ["Maximize"],
            "/",
            ["Bold", "Italic", "Underline", "Subscript", "Superscript"],
            ["Font", "FontSize", "TextColor", "BGColor"],
            ["Scayt"],
            ["PasteFromWord", "youtube"],
        ],
        "extraPlugins": ",".join(
            [
                "autolink",
                "autoembed",
                "autogrow",
                "scayt",
                "autosave",
                "notification",
                "tableresize",
                "undo",
                "autoembed",
                "embedbase",
                "youtube",
            ]
        ),
    }
}

# Error Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "debug.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
