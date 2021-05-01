import uuid

from django.conf import settings
from django.db import models
from django.urls import reverse
from django_extensions.db import fields
from tagging import fields as tags_fields
from tagging import registry

from base import managers
from base import models as base_models


class Term(base_models.BaseModel):
    value = models.CharField(max_length=255, unique=True)
    slug = fields.AutoSlugField(populate_from=('value',))

    objects = managers.ActiveManager()
    all_objects = models.Manager()

    def __str__(self):
        return self.value

    @property
    def definitions(self):
        return self.definition_set.all()

    def get_absolute_url(self):
        return reverse('term-detail', kwargs={'slug': self.slug})


class Definition(base_models.BaseModel):
    term = models.ForeignKey(Term, on_delete=models.CASCADE)
    value = models.TextField()
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             blank=True,
                             null=True,
                             on_delete=models.PROTECT)
    tags = tags_fields.TagField()

    objects = managers.ActiveManager()
    all_objects = models.Manager()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.value

    def get_absolute_url(self):
        return reverse('definition-detail', kwargs={'uuid': self.uuid})

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


registry.register(
    Definition, tag_descriptor_attr='assigned_tags'
)
