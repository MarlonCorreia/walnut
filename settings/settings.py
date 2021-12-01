###
# Project Settings
###

import os
import dj_database_url
from pathlib import Path
from s3_environ import S3Environ

import dotenv


###
# Enviroment
###

###
# Get data from .env file
###
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))

ENVIRONMENT = os.environ.get('ENVIRONMENT')
LOAD_ENVS_FROM_FILE = True if os.environ.get('LOAD_ENVS_FROM_FILE', False) == 'True' else False

env_file = 'envs-production.json'
if not LOAD_ENVS_FROM_FILE:
    S3Environ(bucket='walnut-envs', key=env_file)
    print("Loading envs from S3: {0}".format(env_file))



###
# Security
###

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = ENVIRONMENT == 'development' or os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [
    'localhost',

    #aws
    '.us-east-1.elb.amazonaws.com',
    '.compute-1.amazonaws.com'
]

###
# Application definition
###

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    
    # Rest Auth
    'rest_auth',
    'rest_auth.registration',
    'rest_framework.authtoken',

    # Allauth
    'allauth',
    'allauth.account',

    #Accounts
    'accounts',
    'walnut'
]
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'settings.wsgi.application'

###
# Authentication
###
AUTH_USER_MODEL = 'accounts.User'
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'accounts.api.v1.serializers.UserTokenSerializer',
    'USER_DETAILS_SERIALIZER': 'accounts.api.v1.serializers.UserDetailsSerializer'
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER': 'accounts.api.v1.serializers.RegisterSerializer'
}

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = 'none'

###
# Database
###

DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASES = {'default': dj_database_url.parse(DATABASE_URL)}
DATABASES['default']['ATOMIC_REQUESTS'] = True

###
# Celery and Redis
###

REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
REDIS_PORT = os.environ.get('REDIS_PORT', '6379')
REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'

CELERY_DEFAULT_QUEUE = ENVIRONMENT
if ENVIRONMENT == 'development':
    CELERY_ALWAYS_EAGER = False
    CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

BROKER_URL = REDIS_URL
VISIBILITY_TIMEOUT = os.environ.get('VISIBILITY_TIMEOUT', 86400)
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': VISIBILITY_TIMEOUT}
ACCEPT_CONTENT = ['json']
TASK_SERIALIZER = 'json'
RESULT_SERIALIZER = 'json'

###
# Rest Framework
###

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
}


###
# Internationalization
###

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

###
# Static files (CSS, JavaScript, Images)
###

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

###
# Defaults primary key field type
###

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
