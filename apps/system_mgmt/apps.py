from django.apps import AppConfig
from django.db.models.signals import post_migrate


class HandleConfig(AppConfig):
    name = "apps.system_mgmt"
    verbose_name = "system_mgmt"

    #
    def ready(self):
        import apps.system_mgmt.nats_api  # noqa
        from apps.system_mgmt.signals.app_singal import init_apps  # noqa

        post_migrate.connect(init_apps, sender=self)
