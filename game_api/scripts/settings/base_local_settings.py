
DEBUG = True

# Make these unique, and don't share it with anybody.
SECRET_KEY = 'DeveloperSecretKey-CONSIDER-CHANGING-THIS-MAYBE'

DATABASES = {
    'sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
    },
    'postgresql': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'silent_night',
        'USER': 'django',
        'PASSWORD': 'elephantdbdj',
        'HOST': 'localhost'
    },
    'docker:pg': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432
    }
}

DATABASES['default'] = DATABASES['docker:pg']


ALLOWED_HOSTS = [
    '127.0.0.1',
    '192.168.1.102',
]


TIME_ZONE = 'America/Los_Angeles'

USE_TZ = True

STATIC_URL = '/static/'

MEDIA_URL = '/media/'