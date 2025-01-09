from django.apps import AppConfig


class NatsDemoConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.nats_demo"

    def ready(self):
        import apps.nats_demo.nats