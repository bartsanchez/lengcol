from django.contrib.admin import site

from definitions import models


site.register(models.Term)
site.register(models.Definition)
