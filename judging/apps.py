# judging/apps.py

from django.apps import AppConfig


class JudgingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "judging"

    def ready(self):
        from . import signals  # noqa
