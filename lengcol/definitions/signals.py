from django import dispatch
from django.db.models import signals

from definitions import models, tasks


@dispatch.receiver(signals.post_save, sender=models.Definition)
def new_definition_handler(sender, instance, created, *args, **kwargs):
    tasks.send_new_definition_mail.delay(pk=instance.pk, created=created)
