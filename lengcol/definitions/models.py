import uuid

from base import managers
from base import models as base_models
from django.conf import settings
from django.db import models
from django_extensions.db import fields


class Term(base_models.BaseModel):
    value = models.CharField(max_length=255, unique=True)
    slug = fields.AutoSlugField(populate_from=('value',))

    def __str__(self):
        return self.value

    @property
    def definitions(self):
        return self.definition_set.all()


class Definition(base_models.BaseModel):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    value = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True,
                             null=True,
                             on_delete=models.PROTECT)

    objects = managers.ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.value

    @property
    def has_examples(self):
        return self.example_set.exists()

    @property
    def examples(self):
        return self.example_set.all()


class Example(base_models.BaseModel):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    value = models.TextField()

    objects = managers.ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.value
