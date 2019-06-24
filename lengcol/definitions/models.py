from django.db import models

from django_extensions.db import fields

from base import models as base_models


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

    def __str__(self):
        return self.value


class Example(base_models.BaseModel):
    definition = models.ForeignKey(Definition, on_delete=models.CASCADE)
    value = models.TextField()

    def __str__(self):
        return self.value
