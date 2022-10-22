from django.apps import AppConfig


class HubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hub'

    def ready(self):
        """Register all signals."""
        # Implicitly connect a signal handlers decorated with @receiver.
        import apps.hub.signals
