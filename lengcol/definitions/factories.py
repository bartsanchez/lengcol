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
        django_get_or_create = ('term', 'value')

    term = factory.SubFactory(TermFactory)
    value = 'definition fake'


class ExampleFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Example
        django_get_or_create = ('definition', 'value')

    definition = factory.SubFactory(DefinitionFactory)
    value = 'example fake'
