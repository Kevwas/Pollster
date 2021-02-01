from pollster.settings.base import *
# For heroku
import django_heroku
import dj_database_url
import os

DEBUG = False

# For heroku
ALLOWED_HOSTS = ['*']

# For heroku
DATABASES = {
    'default': dj_database_url.config()
}

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

# For heroku
django_heroku.settings(locals())



