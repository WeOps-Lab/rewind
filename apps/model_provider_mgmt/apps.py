from django.apps import AppConfig
from django.db.models.signals import post_migrate


class EmbedMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.model_provider_mgmt"
    verbose_name = "模型供应商"

    def ready(self):
        from apps.model_provider_mgmt.signals import user_create_signal

        post_migrate.connect(user_create_signal, sender=self)
