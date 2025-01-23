from django.db import migrations


def run_init_apps(apps, schema_editor):
    from apps.system_mgmt.signals.app_singal import init_apps

    init_apps()


class Migration(migrations.Migration):
    dependencies = [
        ("base", "0004_alter_userapisecret_options_and_more"),
    ]

    operations = [
        migrations.RunPython(run_init_apps),
    ]
