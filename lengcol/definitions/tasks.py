import os

from django.conf import settings
from django.contrib import sitemaps
from django.core import mail

from definitions import models
from lengcol.celery import app


@app.task()
def send_new_definition_mail(pk):
    definition = models.Definition.objects.get(pk=pk)
    mail_content = {
        'subject': 'New definition was created',
        'message': f'{settings.BASE_URL}{definition.get_absolute_url()}',
        'from_email': f'{settings.APP_EMAIL}',
        'recipient_list': [f'{settings.APP_EMAIL}'],
        'fail_silently': True,
    }
    mail.send_mail(**mail_content)


@app.task()
def ping_google_for_sitemap():
    django_settings_module = os.environ.get('DJANGO_SETTINGS_MODULE')
    if 'prod' in django_settings_module:
        sitemaps.ping_google()
