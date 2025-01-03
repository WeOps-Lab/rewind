# Generated by Django 4.2.7 on 2024-11-28 02:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("model_provider_mgmt", "0002_skillrule"),
    ]

    operations = [
        migrations.CreateModel(
            name="TokenConsumption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("input_tokens", models.BigIntegerField()),
                ("output_tokens", models.BigIntegerField()),
                ("username", models.CharField(max_length=100)),
                ("user_id", models.CharField(max_length=100)),
            ],
        ),
    ]