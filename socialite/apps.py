# apps.py
from django.apps import AppConfig

class SocialiteConfig(AppConfig):
    name = 'socialite'

    def ready(self):
        import socialite.signals  # Import signals to ensure they're connected
