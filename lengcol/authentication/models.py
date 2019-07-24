from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth import validators


class User(auth_models.AbstractUser):
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        validators=[validators.UnicodeUsernameValidator()],
        error_messages={'unique': 'A user with that username already exists.'},
    )
