'''Use this for production'''
import django_heroku
from .base import *
import dj_database_url
# from home.aws.conf import *

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
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]


'''
https://rk-mcq.herokuapp.com// | https://git.heroku.com/rkmcq.git
'''

STRIPE_SECRET_KEY = ''

# S3 BUCKETS CONFIG
'''
# AWS_ACCESS_KEY_ID = 'AKIAQ7KLZJXGOENX2XTT'
# AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'rkx-test'

AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

AWS_S3_FILE_OVERWRITE = False

'''
'''
<?xml version = "1.0" encoding = "UTF-8"?>
<CORSConfiguration xmlns = "http://s3.amazonaws.com/doc/2006-03-01/" >
<CORSRule >
    <AllowedOrigin > * < /AllowedOrigin >
    <AllowedMethod > GET < /AllowedMethod >
    <AllowedMethod > POST < /AllowedMethod >
    <AllowedMethod > PUT < /AllowedMethod >
    <AllowedHeader > * < /AllowedHeader >
</CORSRule >
</CORSConfiguration >
'''
# CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ['http://localhost:3000', '127.0.0.1']
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static_files'),
]

AWS_ACCESS_KEY_ID = 'AKIAQ7KLZJXGHOYLWLWI'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'rk-s3-bucket'
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

AWS_LOCATION = 'static_files'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)
# STATIC_URL = 'https://rk-s3-bucket.s3.amazonaws.com/'
STATIC_URL = 'https://rk-s3-bucket.s3.ap-south-1.amazonaws.com/'
DEFAULT_FILE_STORAGE = 'home.settings.storage_backends.MediaStorage'
AWS_DEFAULT_ACL = None
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'


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
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

django_heroku.settings(locals())
