from datetime import timedelta

from django.conf import settings
from .base import *

SITE_NAME = 'Konotasi'
SITE_DOMAIN = 'www.konotasi.com'


# Application definition
PROJECT_APPS = [
    'corsheaders',
    'rest_framework',
    'apps.person.apps.PersonConfig',
    'apps.debate.apps.DebateConfig',
]

INSTALLED_APPS = INSTALLED_APPS + PROJECT_APPS


# Application middleware
PROJECT_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
]

MIDDLEWARE = MIDDLEWARE + PROJECT_MIDDLEWARE


# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
try:
    AUTH_USER_APP_LABEL, AUTH_USER_MODEL_NAME = AUTH_USER_MODEL.rsplit('.', 1)
except ValueError:
    raise ImproperlyConfigured("AUTH_USER_MODEL must be of the form"
                               " 'app_label.model_name'")


# Caching
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'temporary_cache',
    }
}


# Django Email
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/topics/email/
DEFAULT_FROM_EMAIL = '%s <teste.coenocyte@gmail.com>' % SITE_NAME
DEFAULT_TO_EMAIL = 'hellopuyup@gmail.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'teste.coenocyte@gmail.com'
EMAIL_HOST_PASSWORD = 'ind0nesi@'


# Django Rest Framework (DRF)
# ------------------------------------------------------------------------------
# https://www.django-rest-framework.org/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.'
                                'NamespaceVersioning',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.'
                                'PageNumberPagination',
    'PAGE_SIZE': 2
}


# Django Sessions
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/ref/settings/
SESSION_COOKIE_HTTPONLY = False
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
AUTO_LOGGED_IN = False


# Static files (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')


# Django Simple JWT
# ------------------------------------------------------------------------------
# https://github.com/davesque/django-rest-framework-simplejwt
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=365),
}


# Django Debug Toolbar
# ------------------------------------------------------------------------------
# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html
if DEBUG:
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    INTERNAL_IPS = ('127.0.0.1', 'localhost',)
    MIDDLEWARE += (
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    INSTALLED_APPS += (
        'debug_toolbar',
    )

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ]

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }