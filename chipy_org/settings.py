# -*- coding: utf-8 -*-
# Django settings for account project

import os
import sys

import dj_database_url
from django.conf.global_settings import MIDDLEWARE_CLASSES


def env_var(key, default=None):
    """Retrieves env vars and makes Python boolean replacements"""
    val = os.environ.get(key, default)
    if val == 'True':
        val = True
    elif val == 'False':
        val = False
    return val


def env_list(key, defaults=[], delimiter=','):
    val_list = defaults
    val = os.environ.get(key, None)
    if val:
        val_list = val.split(delimiter)
    return val_list


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(os.path.join(PROJECT_ROOT, 'apps'))

DEBUG = env_var('DEBUG', False)
TEMPLATE_DEBUG = DEBUG

GITHUB_APP_ID = env_var('GITHUB_APP_ID')
GITHUB_API_SECRET = env_var('GITHUB_API_SECRET')

# tells Pinax to serve media through the staticfiles app.
SERVE_MEDIA = env_var('SERVE_MEDIA', DEBUG)

INTERNAL_IPS = [
    "127.0.0.1",
]

ADMINS = [(admin.split('@')[0], admin) for admin in env_var('ADMINS').split(',')]

MANAGERS = ADMINS


ALLOWED_HOSTS=env_list("ALLOWED_HOSTS", ['www.chipy.org', 'chipy.org'])

# dj_database_url will pull from the DATABASE_URL environment variable
DATABASES = {'default': dj_database_url.config(default='postgres://localhost:5432/chipy_org')}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = "US/Central"

LOGIN_URL = "/login/"

LOGIN_REDIRECT_URL = '/'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = "en-us"

SITE_ID = env_var('SITE_ID', 1)

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# Additional directories which hold static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATIC_URL = '/static/'

MEDIA_URL = STATIC_URL + 'media/'

STATIC_ROOT = 'staticfiles'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = os.path.join(STATIC_URL, "admin/")

# Make this unique, and don't share it with anybody.
SECRET_KEY = env_var('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = [
    "django.template.loaders.filesystem.Loader",
    "django.template.loaders.app_directories.Loader",
]

ROOT_URLCONF = "chipy_org.urls"

TEMPLATE_DIRS = [
    os.path.join(PROJECT_ROOT, "templates"),
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "social_auth.context_processors.social_auth_login_redirect",
]

# Social Auth settings
MIDDLEWARE_CLASSES += ('chipy_org.libs.middleware.ChipySocialAuthExceptionMiddleware',)
LOGIN_ERROR_URL = '/'

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.twitter.TwitterBackend',
    'social_auth.backends.facebook.FacebookBackend',
    'social_auth.backends.google.GoogleBackend',
    'social_auth.backends.browserid.BrowserIDBackend',
    'social_auth.backends.contrib.linkedin.LinkedinBackend',
    'social_auth.backends.contrib.github.GithubBackend',
    'social_auth.backends.OpenIDBackend',
    'django.contrib.auth.backends.ModelBackend',
)

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

SOCIAL_AUTH_ENABLED_BACKENDS = (
    'google',
    'github',
)

SOCIAL_AUTH_PIPELINE = (
    'social_auth.backends.pipeline.social.social_auth_user',
    'social_auth.backends.pipeline.user.get_username',
    'chipy_org.libs.social_auth_pipelines.create_user', # Custom pipeline addition. Located in libs/
    'social_auth.backends.pipeline.social.associate_user',
    'social_auth.backends.pipeline.social.load_extra_data',
    'social_auth.backends.pipeline.user.update_user_details'
)

SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email', 'first_name', 'last_name']

GITHUB_EXTRA_DATA = [
    ('email', 'email'),
]

INSTALLED_APPS = [
    # Fancy Admin
    'grappelli',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.flatpages',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    # Third party
    'nocaptcha_recaptcha',
    'django_ical',
    'envelope',
    'flatblocks',
    'flatpages_tinymce',
    'django_gravatar',
    'gunicorn',
    'honeypot',
    'interval',
    'rest_framework',
    'social_auth',
    'south',
    'storages',
    'tinymce',

    # theme
    'django_forms_bootstrap',

    # project
    'about',
    'contact',
    'meetings',
    'profiles',
]

if DEBUG:
    # Add the command extensions
    INSTALLED_APPS += ['django_extensions']

FIXTURE_DIRS = [
    os.path.join(PROJECT_ROOT, "fixtures"),
]

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

ENVELOPE_EMAIL_RECIPIENTS = env_var('ENVELOPE_EMAIL_RECIPIENTS').split(',')

EMAIL_BACKEND = env_var('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = env_var('EMAIL_HOST', 'smtp.sendgrid.net')
EMAIL_HOST_USER = env_var('EMAIL_HOST_USER', env_var('SENDGRID_USERNAME', None))
EMAIL_HOST_PASSWORD = env_var('EMAIL_HOST_PASSWORD', env_var('SENDGRID_PASSWORD', None))
EMAIL_PORT = int(env_var('EMAIL_PORT', 587))
EMAIL_USE_TLS = env_var('EMAIL_USE_TLS', True)

DEFAULT_FROM_EMAIL = env_var('DEFAULT_FROM_EMAIL', 'DoNotReply@chipy.org')
HONEYPOT_FIELD_NAME = 'email2'

if env_var('PRODUCTION', False):
    PREPEND_WWW = True

TINYMCE_DEFAULT_CONFIG = {
    'height': "500",
    # custom plugins
    'plugins': "table,spellchecker,paste,searchreplace,inlinepopups",
    # editor theme
    'theme': "advanced",
    # custom CSS file for styling editor area
    'content_css': MEDIA_URL + "css/custom_tinymce.css",
    # use absolute urls when inserting links/images
    'relative_urls': False,
}

NORECAPTCHA_SITE_KEY = env_var('NORECAPTCHA_SITE_KEY')
NORECAPTCHA_SECRET_KEY = env_var('NORECAPTCHA_SECRET_KEY')

FLATPAGES_TINYMCE_ADMIN = True

MEETUP_API_KEY = env_var('MEETUP_API_KEY')