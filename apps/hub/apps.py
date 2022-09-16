from django.apps import AppConfig


class HubConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.hub'

    def ready(self):
        """Register all signals."""
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals

        # Explicitly connect a signal handler.
        # request_finished.connect(signals.my_callback)
