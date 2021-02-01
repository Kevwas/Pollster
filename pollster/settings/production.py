from pollster.settings.base import *
# For heroku
import django_heroku
import dj_database_url
import os

DEBUG = False

if DEBUG:
    SECRET_KEY = '_rl8(m5j#opso1r4h&0!8f3==%!i9m3jslar^5z5w(aw9d1nks'
else:
    SECRET_KEY = os.environ['SECRET_KEY']

# For heroku
ALLOWED_HOSTS = ['*']

# For heroku
DATABASES = {
    'default': dj_database_url.config()
}

# For heroku
django_heroku.settings(locals())

# STATICFILES_DIRS = []

# STATIC_ROOT = BASE_DIR / 'static'

