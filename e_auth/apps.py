from django.apps import AppConfig


class EAuthConfig(AppConfig):
    name = 'e_auth'
    def ready(self):
        import e_auth.signals