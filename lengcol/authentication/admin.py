from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from authentication import models

admin.site.register(models.User, auth_admin.UserAdmin)
