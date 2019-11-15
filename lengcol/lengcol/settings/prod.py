from lengcol.settings.base import *


SECRET_KEY = os.environ.get('SECRET_KEY')

ADMINS = [
    ('Bart', 'bsanchezsalado@gmail.com'),
]

DEBUG = False

ALLOWED_HOSTS = [
    'www.lenguajecoloquial.com',
    'www.lenguajecoloquial.es',
]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

EMAIL_HOST = 'smtp.ionos.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'info@lenguajecoloquial.com'
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
