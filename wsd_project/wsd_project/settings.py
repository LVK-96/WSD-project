"""
Django settings for wsd_project project.

Generated by 'django-admin startproject' using Django 2.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os 

# this line is already in your settings.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
if os.getenv('SECRET_KEY'):
    SECRET_KEY = os.getenv('SECRET_KEY')
else:
    SECRET_KEY = '0irbi1%r19s0i!ycb!9-7@nvw6xtq8k$-3xhd7e^8z0drni!uk'

# SECURITY WARNING: don't run with debug turned on in production!
if os.getenv('DEBUG'):
    DEBUG = True
else:
    DEBUG = True


if os.getenv('PAYMENT_SUCCESS_URL'):
    PAYMENT_SUCCESS_URL = os.getenv('PAYMENT_SUCCESS_URL')
else:
    PAYMENT_SUCCESS_URL = 'http://127.0.0.1:8000/payment/success'

if os.getenv('PAYMENT_CANCEL_URL'):
    PAYMENT_CANCEL_URL = os.getenv('PAYMENT_CANCEL_URL')
else:
    PAYMENT_CANCEL_URL = 'http://127.0.0.1:8000/payment/cancel'

if os.getenv('PAYMENT_ERROR_URL'):
    PAYMENT_ERROR_URL = os.getenv('PAYMENT_ERROR_URL')
else:
    PAYMENT_ERROR_URL = 'http://127.0.0.1:8000/payment/error'

ALLOWED_HOSTS = []
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store.apps.StoreConfig',    
    'users.apps.UsersConfig',
    'social_django' 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'wsd_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'wsd_project.wsgi.application'

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
   }
} 

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
 'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
 'social_core.backends.google.GoogleOpenId',  # for Google authentication
 'social_core.backends.google.GoogleOAuth2',  # for Google authentication
 'django.contrib.auth.backends.ModelBackend',
)

if os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'):
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY')
else:
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='538988683043-6v2g2t3c1bpd039rn6vv4fvbr3hh8oe2.apps.googleusercontent.com'  #Paste CLient Key

if os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'):
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET')
else:
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'ojJRE1pmjr5SBY9D_il90tKI' #Paste Secret Key

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

EMAIL_HOST = 'smtp.sendgrid.net'

if os.getenv('EMAIL_HOST_USER'):
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USERNAME') 
else:
    EMAIL_HOST_USER = 'app119607950@heroku.com'

if os.getenv('EMAIL_HOST_PASSWORD'):
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
else:
    EMAIL_HOST_PASSWORD = 'oaepgzhz4672'

EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "media"),
    os.path.join(BASE_DIR, "store/static"),
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Redirect after login and logout
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'index'
# default redirect when login required
LOGIN_URL = 'login'

AUTH_USER_MODEL = 'users.CustomUser'

# Configure Django App for Heroku.
import django_heroku
django_heroku.settings(locals())

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)