# kct/apps.py

from django.apps import AppConfig


class KctConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kct"

    def ready(self):
        from . import signals  # noqa

