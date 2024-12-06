from django.apps import AppConfig


class RentalSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'rental_system'

    def ready(self):
        import rental_system.signals
