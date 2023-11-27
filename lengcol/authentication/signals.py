from django import dispatch
from django.db.models import signals

from authentication import models, tasks


@dispatch.receiver(signals.post_save, sender=models.User)
def new_registered_user_handler(sender, instance, created, *args, **kwargs):
    if created:
        tasks.send_new_registered_user_mail.delay(pk=instance.pk)
