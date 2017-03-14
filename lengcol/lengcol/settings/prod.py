from lengcol.settings.base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = [
    'lengcol.herokuapp.com',
    'www.lenguajecoloquial.com',
    'www.lenguajecoloquial.es',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
