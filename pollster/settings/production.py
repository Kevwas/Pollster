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


# For heroku
django_heroku.settings(locals())



