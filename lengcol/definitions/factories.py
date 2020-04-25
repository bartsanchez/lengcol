import datetime

import factory
from factory import django

from definitions import models


class TermFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Term
        django_get_or_create = ('value',)

    value = 'term fake'


class DefinitionFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Definition
        django_get_or_create = ('uuid', 'term', 'value')

    uuid = factory.Faker('uuid4')
    term = factory.SubFactory(TermFactory)
    value = 'definition fake'
    created = datetime.datetime(year=2020, month=1, day=1)


class ExampleFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Example
        django_get_or_create = ('definition', 'value')

    definition = factory.SubFactory(DefinitionFactory)
    value = 'example fake'
