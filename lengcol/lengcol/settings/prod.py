from lengcol.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY')

ADMINS = [
    ('Bart', 'bsanchezsalado@gmail.com'),
]

DEBUG = False

ALLOWED_HOSTS = [
    'lenguajecoloquial.com',
    'lenguajecoloquial.es',
    'www.lenguajecoloquial.com',
    'www.lenguajecoloquial.es',
]

SESSION_COOKIE_AGE = 7200  # 2 hours

# SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

CELERY_TASK_ALWAYS_EAGER = False

EMAIL_HOST = 'smtp.ionos.es'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@lenguajecoloquial.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    },
    'handlers': {
        'recaptcha_logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/gunicorn/recaptcha.log',
            'maxBytes': 1024*1024,  # 1MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'snowpenguin.django.recaptcha3': {
            'handlers': ['recaptcha_logfile'],
            'level': 'DEBUG',
        },
    },
}
