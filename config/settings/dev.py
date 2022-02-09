from .base import *


ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': SESNSITIVE_.get("DB_NAME"),
        'USER': SESNSITIVE_.get("DB_USER"),
        'PASSWORD': SESNSITIVE_.get("DB_PASSWORD"),
        'HOST': SESNSITIVE_.get("DB_HOST"),
        'PORT': SESNSITIVE_.getint("DB_PORT")
    }
}


# Cors Settings
# If True, all origins will be allowed
CORS_ALLOW_ALL_ORIGINS = ENV_INFO_.getboolean("CORS_ALLOW_ALL")


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}
