from django import dispatch
from django.conf import settings
from django.core import mail
from django.db.models import signals

from definitions import models


@dispatch.receiver(signals.post_save, sender=models.Definition)
def new_definition_handler(sender, instance, *args, **kwargs):
    mail_content = {
        'subject': 'New definition was created',
        'message': f'{settings.BASE_URL}{instance.get_absolute_url()}',
        'from_email': f'{settings.APP_EMAIL}',
        'recipient_list': [f'{settings.APP_EMAIL}'],
        'fail_silently': True,
    }
    mail.send_mail(**mail_content)
