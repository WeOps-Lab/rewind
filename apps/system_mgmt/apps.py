from django.apps import AppConfig


class HandleConfig(AppConfig):
    name = "apps.system_mgmt"
    verbose_name = "system_mgmt"
    #
    # def ready(self):
    #     from apps.system_mgmt.signals.app_singal import init_apps
    #
    #     post_migrate.connect(init_apps, sender=self)
