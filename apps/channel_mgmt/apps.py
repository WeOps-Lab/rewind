from django.apps import AppConfig
from django.db.models.signals import post_migrate


class ChannelMgmtConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.channel_mgmt"
    verbose_name = "channel management"

    def ready(self):
        from apps.channel_mgmt.signals.user_create_signal import user_create_signal

        post_migrate.connect(user_create_signal, sender=self)
