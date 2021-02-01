from pollster.settings.base import *
# For heroku
import django_heroku
import dj_database_url
import os

DEBUG = True

# For heroku
ALLOWED_HOSTS = ['*']

# For heroku
DATABASES = {
    'default': dj_database_url.config()
}

# For heroku
django_heroku.settings(locals())

STATICFILES_DIRS = []

STATIC_ROOT = BASE_DIR / 'static'

