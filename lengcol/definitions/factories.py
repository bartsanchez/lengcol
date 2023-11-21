import factory
from definitions import models
from factory import django
from tagging import models as tagging_models


class TermFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Term
        django_get_or_create = ("value",)

    value = "term fake"


class DefinitionFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Definition
        django_get_or_create = ("uuid", "term", "value")

    uuid = factory.Faker("uuid4")
    term = factory.SubFactory(TermFactory)
    value = "definition fake"
    tags = "fake tag 1, another fake tag 2"


class ExampleFactory(django.DjangoModelFactory):
    class Meta:
        model = models.Example
        django_get_or_create = ("definition", "value")

    definition = factory.SubFactory(DefinitionFactory)
    value = "example fake"


class TagFactory(django.DjangoModelFactory):
    class Meta:
        model = tagging_models.Tag
        django_get_or_create = ("name",)

    name = "tag fake"
