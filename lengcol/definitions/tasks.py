from django.conf import settings
from django.core import mail

from definitions import models
from lengcol.celery import app


@app.task()
def send_new_definition_mail(pk, created):
    action = "created" if created else "updated"
    definition = models.Definition.objects.get(pk=pk)
    message = (
        f"Término: --{definition.term}--",
        f"Definición: --{definition.value}--",
        f"URL: {settings.BASE_URL}{definition.get_absolute_url()}",
    )
    mail_content = {
        "subject": f"New definition was {action}",
        "message": "\n".join(message),
        "from_email": f"{settings.APP_EMAIL}",
        "recipient_list": [f"{settings.APP_EMAIL}"],
        "fail_silently": True,
    }
    mail.send_mail(**mail_content)
