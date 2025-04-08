import os
import logging
print("DEBUG ENV:", os.environ)

print("RDS_DB_NAME:", os.environ.get('RDS_DB_NAME'))


from pathlib import Path




# Log RDS env vars to EB logs
logging.warning(f"📦 RDS_DB_NAME: {os.environ.get('RDS_DB_NAME')}")
logging.warning(f"📦 RDS_USERNAME: {os.environ.get('RDS_USERNAME')}")


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-m10c@k!u5b!y@=n%!9dxmc4#=q)q$)tdu$6$&w#1p_y107=2c_'
)



# DEBUG = os.environ.get("DJANGO_DEBUG", "False").lower() in ("true", "1", "yes")





ALLOWED_HOSTS = ['mydemo-dev.us-west-2.elasticbeanstalk.com']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'images.apps.ImagesConfig',
    'django_tables2',
    'crispy_forms',
    'crispy_bootstrap4',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

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

WSGI_APPLICATION = 'core.wsgi.application'

# Database settings


if os.environ.get('RDS_DB_NAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('RDS_DB_NAME'),
            'USER': os.environ.get('RDS_USERNAME'),
            'PASSWORD': os.environ.get('RDS_PASSWORD'),
            'HOST': os.environ.get('RDS_HOSTNAME'),
            'PORT': os.environ.get('RDS_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

print("Using DB:", DATABASES['default'])





if os.environ.get('RDS_DB_NAME'):
    print("✅ Using RDS PostgreSQL DB")
else:
    print("⚠️ Using SQLite DB")

# Optional: log DB engine to Django log
logger = logging.getLogger(__name__)
logger.info("Database Engine: %s", DATABASES['default']['ENGINE'])




# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# S3 configuration
# S3 configuration
USE_S3 = all([
    os.environ.get('AWS_ACCESS_KEY_ID'),
    os.environ.get('AWS_SECRET_ACCESS_KEY'),
    os.environ.get('AWS_STORAGE_BUCKET_NAME'),
])

if USE_S3:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    
    # Use AWS_REGION if S3 region is not explicitly defined
    AWS_REGION = os.environ.get('AWS_REGION', 'us-west-2')
    AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', AWS_REGION)
    
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'
    AWS_LOCATION = 'media'

    # Static files (CSS, JS)
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'

    # Media files (user uploads)
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/'
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = BASE_DIR / 'staticfiles'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'mediafiles'


# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Tables and Forms
DJANGO_TABLES2_TEMPLATE = 'django_tables2/bootstrap4.html'
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap4"]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
