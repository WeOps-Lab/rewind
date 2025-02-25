# Generated by Django 4.2.7 on 2025-02-24 02:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("model_provider_mgmt", "0008_llmskill_show_think"),
    ]

    operations = [
        migrations.AddField(
            model_name="embedprovider",
            name="team",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="ocrprovider",
            name="team",
            field=models.JSONField(default=list),
        ),
        migrations.AddField(
            model_name="rerankprovider",
            name="team",
            field=models.JSONField(default=list),
        ),
    ]
