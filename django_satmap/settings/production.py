from .base import *

DEBUG = True

ALLOWED_HOSTS = ['satmapper.herokuapp.com', 'satmapper-fcb6a3f8eafd.herokuapp.com']

if "DATABASE_URL" in os.environ:
    # Configure Django for DATABASE_URL environment variable.
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=MAX_CONN_AGE, ssl_require=True)
    }

    # Enable test database if found in CI environment.
    if "CI" in os.environ:
        DATABASES["default"]["TEST"] = DATABASES["default"]


# SECURE_SSL_REDIRECT = True

# STATIC_URL = 'https://{0}/{1}/'.format(
#     AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'