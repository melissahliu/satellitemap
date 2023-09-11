from .base import *

DEBUG = True

ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1', '.ngrok.io', 'localhost']

INTERNAL_IPS = ['127.0.0.1', 'localhost']

INSTALLED_APPS += ['debug_toolbar']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'satmap',
#         'USER': 'samer',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'