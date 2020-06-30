from django.conf import settings
from django.core import mail

from authentication import models
from lengcol.celery import app


@app.task()
def send_new_registered_user_mail(pk):
    user = models.User.objects.get(pk=pk)
    mail_content = {
        'subject': 'New user was registered',
        'message': f'{user.username}',
        'from_email': f'{settings.APP_EMAIL}',
        'recipient_list': [f'{settings.APP_EMAIL}'],
        'fail_silently': True,
    }
    mail.send_mail(**mail_content)
