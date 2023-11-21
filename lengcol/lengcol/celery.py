import celery

app = celery.Celery("lengcol")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
