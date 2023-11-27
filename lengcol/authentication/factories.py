import factory
from factory import django

from authentication import models


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = models.User
        django_get_or_create = ("username",)

    username = "fake_username"
    password = factory.PostGenerationMethodCall("set_password", "fake_password")
    email = "fake@email.com"
