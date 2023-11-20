from definitions import models, tasks
from django import dispatch
from django.db.models import signals


@dispatch.receiver(signals.post_save, sender=models.Definition)
def new_definition_handler(sender, instance, created, *args, **kwargs):
    if created:
        tasks.send_new_definition_mail.delay(pk=instance.pk)
    tasks.ping_google_for_sitemap.delay()
