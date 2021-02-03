from pollster.settings.base import *
# For heroku
import django_heroku
import dj_database_url
import os

# For heroku
# DEBUG=False

# For heroku
SECRET_KEY = os.environ.get('SECRET_KEY')

# For heroku
ALLOWED_HOSTS = ['*']

# For heroku
DATABASES = {
    'default': dj_database_url.config()
}



SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# For heroku
django_heroku.settings(locals())



