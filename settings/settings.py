###
# Project Settings
###

import os
import dj_database_url
from pathlib import Path

import dotenv


###
# Enviroment
###

ENVIRONMENT = os.environ.get('ENVIRONMENT')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv.read_dotenv(os.path.join(BASE_DIR, '.env'))


###
# Security
###

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = ENVIRONMENT == 'development' or os.environ.get('DEBUG', False)

ALLOWED_HOSTS = [
    'localhost',
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
    'accounts'
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
# Rest Framework
###

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': None,
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

###
# Defaults primary key field type
###

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
