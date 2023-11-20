from definitions import models
from django.contrib import admin


class DefinitionInline(admin.StackedInline):
    model = models.Definition
    extra = 0


class TermAdmin(admin.ModelAdmin):
    inlines = (DefinitionInline,)


admin.site.register(models.Term, TermAdmin)
admin.site.register(models.Definition)
admin.site.register(models.Example)
