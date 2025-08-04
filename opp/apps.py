from django.apps import AppConfig


class OppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'opp'

    def ready(self):
        import opp.signals
