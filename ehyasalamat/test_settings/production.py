from base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ehya',
        'USER': 'ehyauser',
        'PASSWORD': '@#ehyasalamat1400',
        'HOST': 'db',
        'PORT': '5432',
        'CONN_MAX_AGE': 300,
    },
}
