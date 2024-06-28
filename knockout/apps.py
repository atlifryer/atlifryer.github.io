# in knockout/apps.py

from django.apps import AppConfig

class KnockoutConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "knockout"

    def ready(self):
        import knockout.signals  # Add this line to connect the signals
