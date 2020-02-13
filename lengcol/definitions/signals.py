from definitions import models
from django import dispatch
from django.core import mail
from django.db.models import signals


@dispatch.receiver(signals.post_save, sender=models.Definition)
def new_definition_handler(sender, instance, *args, **kwargs):
    mail.send_mail(
        'New definition was created',
        'PK: {}'.format(instance.pk),
        'info@lenguajecoloquial.com',
        ['info@lenguajecoloquial.com'],
        fail_silently=True,
    )
