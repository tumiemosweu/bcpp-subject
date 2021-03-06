# coding=utf-8

import sys
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')78^w@s3^kt)6lu6()tomqjg#8_%!381-nx5dtu#i=kn@68h_^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['10.113.201.173', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crypto_fields.apps.AppConfig',
    'django_revision.apps.AppConfig',
    'edc_base.apps.AppConfig',
    'edc_consent.apps.AppConfig',
    'edc_sync.apps.AppConfig',
    'edc_subset_manager.apps.AppConfig',
    'edc_registration.apps.AppConfig',
    'edc_visit_schedule.apps.AppConfig',
    'bcpp.apps.AppConfig',
    'bcpp.apps.EdcMetadataAppConfig',
    'bcpp.apps.EdcIdentifierAppConfig',
    'bcpp.apps.EdcProtocolAppConfig',
    'bcpp.apps.SurveyAppConfig',
    'bcpp.apps.EdcMapAppConfig',
    'bcpp.apps.EdcDeviceAppConfig',
    'bcpp.apps.EdcBaseTestAppConfig',
    'bcpp.apps.EdcTimepointAppConfig',
    'bcpp.apps.EdcAppointmentAppConfig',
    'household.apps.AppConfig',
    'member.apps.AppConfig',
    'plot.apps.AppConfig',
    'bcpp_lab.apps.AppConfig',
    'bcpp_subject.apps.AppConfig',
    'bcpp_subject.apps.EdcVisitTrackingAppConfig',
]

# if 'test' in sys.argv:
#     INSTALLED_APPS = INSTALLED_APPS = ['example_survey.apps.AppConfig']

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'bcpp_subject.urls'

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

WSGI_APPLICATION = 'bcpp_subject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


if 'test' in sys.argv:  # and 'mysql' not in DATABASES.get('default').get('ENGINE'):
    MIGRATION_MODULES = {
        "django_crypto_fields": None,
        "edc_call_manager": None,
        "edc_appointment": None,
        "edc_call_manager": None,
        "edc_consent": None,
        "edc_death_report": None,
        "edc_export": None,
        "edc_identifier": None,
        "edc_metadata": None,
        "edc_rule_groups": None,
        "edc_registration": None,
        "edc_sync": None,
        "bcpp": None,
        "bcpp_subject": None,
        "plot": None,
        "household": None,
        "member": None,
        "bcpp_subject": None,
        "survey": None,
        'admin': None,
        "auth": None,
        'bcpp_map': None,
        'contenttypes': None,
        'sessions': None,
    }
if 'test' in sys.argv:
    PASSWORD_HASHERS = ('django_plainpasswordhasher.PlainPasswordHasher', )
if 'test' in sys.argv:
    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'bcpp_subject', 'media')
CURRENT_MAP_AREA = 'test_community'
DEVICE_ID = '99'
