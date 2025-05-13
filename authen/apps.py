from django.apps import AppConfig

class AuthenConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authen'

    def ready(self):
        import authen.signals  # Assurez-vous que le fichier `signals.py` existe et est correct
