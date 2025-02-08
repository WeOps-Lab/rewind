# -*- coding: utf-8 -*-

from django.core.management import call_command
from django.db import migrations


def create_cache_table(apps, schema_editor):
    """
    创建 cache table
    """
    call_command("createcachetable", "django_cache")


class Migration(migrations.Migration):
    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [migrations.RunPython(create_cache_table)]
