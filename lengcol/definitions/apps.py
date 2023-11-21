from django.apps import AppConfig


class DefinitionsConfig(AppConfig):
    name = "definitions"

    def ready(self):
        from definitions import signals  # noqa
