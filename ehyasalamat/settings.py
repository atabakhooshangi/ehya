from datetime import timedelta
import locale
from pathlib import Path
import firebase_admin
from decouple import config
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development test_settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # 'jet.dashboard',
    # 'jet',
    # 'jazzmin',
    'django.contrib.flatpages',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'ticket.apps.TicketConfig',
    'informs.apps.InformsConfig',
    'sms.apps.SmsConfig',
    'treasure.apps.TreasureConfig',
    'support.apps.SupportConfig',
    'wphome.apps.WphomeConfig',
    'push_notification.apps.PushNotificationConfig',
    'jalali_date',
    'mptt',
    "fcm_django",
    'tinymce',
    # swagger
    'drf_yasg',
    # api
    'rest_framework',

    'rangefilter',

    # cors
    'corsheaders',
]
SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ehyasalamat.urls'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

locale.setlocale(locale.LC_ALL, "fa_IR.UTF-8")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'ehyasalamat.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'ehya',
        # 'USER': 'postgres',
        # 'PASSWORD': 'postgres',
        'USER': 'ehyauser',
        'PASSWORD': '@#ehyasalamat1400',
        'HOST': '192.167.0.3',
        'PORT': '5432',
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGES = (
    ('fa', 'Farsi'),
    ('en', 'English')
)

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = "accounts.User"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# STATICFILES_DIRS = [BASE_DIR / 'assets']
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1)
}

JALALI_DATE_DEFAULTS = {
    'Strftime': {
        'date': '%y/%m/%d',
        'datetime': '%H:%M:%S _ %y/%m/%d',
    },
    'Static': {
        'js': [
            # loading datepicker
            'admin/js/django_jalali.min.js',
            # OR
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.core.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/calendar.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc.js',
            # 'admin/jquery.ui.datepicker.jalali/scripts/jquery.ui.datepicker-cc-fa.js',
            # 'admin/js/main.js',
        ],
        'css': {
            'all': [
                'admin/jquery.ui.datepicker.jalali/themes/base/jquery-ui.min.css',
            ]
        }
    },
}

CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logging/logs.log',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logging/error_logs.log',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'ehya': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 9015165

FCM_DJANGO_SETTINGS = {
    "FCM_SERVER_KEY": "AAAAb0PN1lM:APA91bGGutURh6gKb_0cXHlAm2tbwOh5p8I5u54BJrysROarQQz7Cs0FoIoKtUSgr3qmZpOHgNFUMYZngl_KLbkBqV6wB-CprVSCl1x2llqUNatBUUweu3zHUCaVuKVsI9CU7XsCW4I8",
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": False,
}
cert = {
    "type": "service_account",
    "project_id": "ehya-app",
    "private_key_id": "e68d85646143f9d0f222cf30dd25d7b271d5fe59",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/s01UDrTqoIQP\nkFQeVWb15Ak+XuWyUi/u9iFVezQ+lsOky0XZEGfz3jN8YbBZPeGs2McfuEFbp4es\nW65Dmetm3zIohdWP/8Xg07hCYTOWP9QQZkq2KDVLjohatRFVglJ02MlgBHbLq1re\no/tX+2TYgEFQ0/UQ5K2xXouy6GFHYgaUkVqa4c+/A0Pt4DjPiKgsfuK9V1XvAudZ\nItSW5xeNkt9ZiWb6+UzJIfg2zatx/HJcmUpeGiFBaCilP6XrSZEBm9Jpn1k2H0po\nnk0pso/OOQYa8mBvVxVzi9n/cQDYksarwAu6yqlNGQIJPjdibrXQ7pCSbP8u5u5x\norqwHDt3AgMBAAECggEAO94QMUcigv+8HmwxiQOc0v/zTxIt4+G87IDbaim+6CkH\nUojU+HQiMsvbAmYzv7sOpn9QuHw/lRMd0NsU8jG4jXj43iTlzEHRl2QncDuQ88Rd\nQv3fKUInWsBZnxJbJnw7qhgl06GxQ+vwxgUqMpDlLqPnQgnfx/XStMjVEft2nebZ\nybW4In/aL3PtkSq79MtlubX8kbQFh+9L5+Czcyx//56ZG6ItxdBVsvV9/tVVTRKR\n51gLNxuK8Qr4TrgtMSzTGOJcUBOFXRcAMKXDdtFAvzg+QsJyKE7a0tvJCbJHn+l4\nhx5DCbqIJnQo96ozkAb9k0P4eNdYKVEr49XhCgJpQQKBgQDhZsz1fAEyrejpTTUa\nf00x/aFQV7Vf8eCbYOHBh12fk+F3Mer68tGLE6xqoGhiHA5q5+zkj3GLtI+718lc\nJQCoiYrwTigMVHZamGLxrP4kl99gsT0oDnebMM1zh7DtpmcnBhnuRMUeeyyRjbHQ\nsP9aOtKf81i7eD5u3DkQvs4bFwKBgQDZuU/ZFDiF9fjITvzhmxNKyqsC4oEpgnIc\npmg7k1I+cymi9tWTsdL75F/DyvZge5fDHQsgNhCP46bQa3Gcf2bvrV564uUKG0Eh\nP8pvLgu9/xcZD7EhlFsBHMZIFHiGirNN40cz8BrB2um1F0H2q0yXNWDf3PVOrLkE\nzj08uYOeoQKBgAQaY/bACCGNCuVcU3AlCxmy3UHiJtoVRBpv/AwS08B456zMytNA\nolHezM+wFdZbXmPRzv0mI1IAunEX74Fu5wEqZ84SDiaTTwg9J+fwVzwBS76t20gk\nY0b+725/9NeOpOgP817j/5abdWc85hS/dBaHZZglzOK0wKYx+hP09TmHAoGAdL5l\n70tlZ4dV5+patIoXlSIJApn7kgttLqmX+GHtVqkfqU9bhD90lzaElxLMez2qSafY\nIGR9CvqRpu4F1FmIE3pNz+y7zWiBytdOr8Dr8OvIMdr1KsFG7tjEBUBcxB+5N0lo\nE5RqdInyiPS4nRCLGAU6Na9gJdh9uPLxaQ88YSECgYAQV2PvadKjPGY4K1l09jAf\nH02Y41vXq4OL5VMr2yrQpgpHR1KkDvNz+1KxulrRh14bdqwtnQkcEYLZmkma4Olb\nLZ1b0U5sAarsRz1EC3UTlsLRaw5H+BEMovUfHWSj8zXk8sb1DUOIU87b9Je1BSFY\nrreRikGUczA47npplO/ldQ==\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-831bg@ehya-app.iam.gserviceaccount.com",
    "client_id": "116012305890151515526",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-831bg%40ehya-app.iam.gserviceaccount.com"
}

cred = credentials.Certificate(cert=cert)
firebase_admin.initialize_app(cred)
