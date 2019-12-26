from .base import *
from .project import *

DEBUG = False
ALLOWED_HOSTS = ['localhost', '::1', '127.0.0.1', 'diskusi-publik.herokuapp.com']

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
    'rest_framework_simplejwt.authentication.JWTAuthentication'
]


# Django Sessions
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/ref/settings/
SESSION_COOKIE_SECURE = False


# Django csrf
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/ref/csrf/
CSRF_TRUSTED_ORIGINS = ['diskusi-publik.herokuapp.com']


# Django CORS
# ------------------------------------------------------------------------------
# https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_WHITELIST = ['diskusi-publik.herokuapp.com']


# Static files (CSS, JavaScript, Images)
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

#  Add configuration for static files storage using whitenoise
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'd8btrf1chrlqid',
        'USER': 'mblgmlnxabnoip',
        'PASSWORD': 'fd334241f5f4a93b8fd0de6f3a81ac87e42aef0979da7a4672d78e46eba7a02d',
        'HOST': 'ec2-107-20-155-148.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}
