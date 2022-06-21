from .base import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ithilleldb',
        'USER': 'postgres',
        'PASSWORD': '123',
        'HOST': 'db',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True
    }
}

MEDIA_URL = '/media/'
MEDIA_ROOT = '/media/'

STATIC_URL = '/static/'
STATIC_ROOT = '/static/'
