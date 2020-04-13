from django import dispatch
from django.conf import settings
from django.core import mail
from django.db.models import signals

from definitions import models


@dispatch.receiver(signals.post_save, sender=models.Definition)
def new_definition_handler(sender, instance, *args, **kwargs):
    mail.send_mail(
        'New definition was created',
        f'{settings.BASE_URL}{instance.get_absolute_url()}',
        f'{settings.APP_EMAIL}',
        [f'{settings.APP_EMAIL}'],
        fail_silently=True,
    )
