# Generated by Django 4.2.7 on 2024-12-17 07:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("channel_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="channel",
            name="channel_type",
            field=models.CharField(
                choices=[
                    ("enterprise_wechat", "Enterprise WeChat"),
                    ("enterprise_wechat_bot", "Enterprise WeChat Bot"),
                    ("wechat_official_account", "WeChat Official Account"),
                    ("ding_talk", "Ding Talk"),
                    ("web", "Web"),
                    ("gitlab", "GitLab"),
                ],
                max_length=100,
                verbose_name="channel type",
            ),
        ),
    ]