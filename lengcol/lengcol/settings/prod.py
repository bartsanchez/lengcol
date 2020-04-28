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

# SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_HOST = 'smtp.ionos.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@lenguajecoloquial.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s: %(message)s'
        }
    },
    'handlers': {
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/gunicorn/lengcol.log',
            'maxBytes': 1024*1024,  # 1MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
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
        'lengcol': {
            'handlers': ['logfile'],
            'level': 'DEBUG',
        },
        'snowpenguin.django.recaptcha3': {
            'handlers': ['recaptcha_logfile'],
            'level': 'DEBUG',
        },
    },
}
