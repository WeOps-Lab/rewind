# Generated by Django 4.2.7 on 2025-02-18 03:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("model_provider_mgmt", "0006_skillrequestlog_user_message_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="llmmodel",
            name="is_build_in",
            field=models.BooleanField(default=True, verbose_name="是否内置"),
        ),
        migrations.AddField(
            model_name="llmmodel",
            name="team",
            field=models.JSONField(default=list),
        ),
        migrations.AlterField(
            model_name="llmmodel",
            name="llm_model_type",
            field=models.CharField(
                choices=[
                    ("chat-gpt", "OpenAI"),
                    ("zhipu", "智谱AI"),
                    ("hugging_face", "Hugging Face"),
                    ("deep-seek", "DeepSeek"),
                ],
                max_length=255,
                verbose_name="LLM模型类型",
            ),
        ),
    ]
