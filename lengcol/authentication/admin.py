from authentication import models
from django.contrib import admin
from django.contrib.auth import admin as auth_admin

admin.site.register(models.User, auth_admin.UserAdmin)
