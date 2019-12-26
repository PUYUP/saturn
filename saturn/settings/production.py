from .base import *
from .project import *

DEBUG = True
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
CSRF_TRUSTED_ORIGINS = [
    'diskusi-publik.herokuapp.com',
    'opsional001.firebaseapp.com'
]


# Django CORS
# ------------------------------------------------------------------------------
# https://pypi.org/project/django-cors-headers/
CORS_ORIGIN_ALLOW_ALL = True
"""
CORS_ORIGIN_WHITELIST = [
    'https://diskusi-publik.herokuapp.com',
    'https://opsional001.firebaseapp.com'
]
"""


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
        'NAME': 'ddkmarkuh0j349',
        'USER': 'guwpftsjmkwkpz',
        'PASSWORD': '6a9f6e8443ffcfea87206cccda8752712af30e7fea9d7cc57c8bf2ce399b441f',
        'HOST': 'ec2-54-235-92-244.compute-1.amazonaws.com',
        'PORT': '5432'
    }
}
