from django.apps import AppConfig


class PantryConfig(AppConfig):
    name = 'pantry'

    def ready(self):
        import pantry.signals
