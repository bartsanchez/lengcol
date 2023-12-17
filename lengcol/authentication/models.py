from django.contrib.auth import models as auth_models
from django.contrib.auth import validators
from django.db import models


class User(auth_models.AbstractUser):
    username = models.CharField(
        "username",
        unique=True,
        validators=[validators.UnicodeUsernameValidator()],
        error_messages={"unique": "A user with that username already exists."},
    )
