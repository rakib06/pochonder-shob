'''Use this for production'''
import django_heroku
from .base import *
import dj_database_url


# WSGI_APPLICATION = 'home.wsgi.prod.application'
WSGI_APPLICATION = 'home.wsgi.prod.application'

CORS_ORIGIN_ALLOW_ALL = True
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PROJECT_ROOT = os.path.join(os.path.abspath(__file__))
MIDDLEWARE += [
    'whitenoise.middleware.WhiteNoiseMiddleware']


'''
https://rk-mcq.herokuapp.com// | https://git.heroku.com/rkmcq.git
'''
# for heroku
if os.getcwd() == '/app':
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)
    # Honor the 'X-forwarded-Proto' header for request.is_secure().
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Allow all host headers
    ALLOWED_HOSTS = ['pochonder-shob.herokuapp.com', 'pochonder-shob.com']
    DEBUG = True

    # Static asset configuration
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

django_heroku.settings(locals())

STRIPE_SECRET_KEY = ''

# S3 BUCKETS CONFIG

AWS_ACCESS_KEY_ID = 'AKIAQ7KLZJXGHUYS5RWN'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'rockib-ps-1'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'


'''
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<CORSRule>
    <AllowedOrigin>*</AllowedOrigin>
    <AllowedMethod>GET</AllowedMethod>
    <AllowedMethod>POST</AllowedMethod>
    <AllowedMethod>PUT</AllowedMethod>
    <AllowedHeader>*</AllowedHeader>
</CORSRule>
</CORSConfiguration>
'''
