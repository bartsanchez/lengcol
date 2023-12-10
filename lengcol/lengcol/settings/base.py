import os

import dj_database_url

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DOMAIN = 'lenguajecoloquial.com'
BASE_SUBDOMAIN = f'www.{BASE_DOMAIN}'
BASE_URL = f'https://{BASE_SUBDOMAIN}'

APP_EMAIL = 'info@lenguajecoloquial.com'

SECRET_KEY = 'rh*dh$k=p*u#l13)pn&2*#iw=nh-p6wmmswgo1$vfvt_xqz6-e'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'base.apps.BaseConfig',
    'definitions.apps.DefinitionsConfig',
    'authentication.apps.AuthenticationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django_extensions',
    'extra_views',
    'crispy_forms',
    'crispy_bootstrap5',
    'snowpenguin.django.recaptcha3',
    'tagging',
]

MIDDLEWARE = [
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'lengcol.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'definitions.context_processors.last_terms',
            ],
        },
    },
]

WSGI_APPLICATION = 'lengcol.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{base_dir}/db.sqlite3'.format(base_dir=BASE_DIR),
    ),
}

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = 'authentication.User'
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

SITE_ID = 1

CELERY_BROKER_URL = 'redis://redis_broker:6379/0'
CELERY_TASK_ALWAYS_EAGER = True

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'

RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', 'fake_private_key')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', 'fake_public_key')
RECAPTCHA_DEFAULT_ACTION = 'generic'
RECAPTCHA_SCORE_THRESHOLD = 0.5

PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(8001, 8004)

FORCE_LOWERCASE_TAGS = True
