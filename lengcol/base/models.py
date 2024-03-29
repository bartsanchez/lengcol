from django.db import models

from base import managers


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class TestModel(BaseModel):
    objects = models.Manager()
    active_objects = managers.ActiveManager()

    def __str__(self):
        return "test instance"
