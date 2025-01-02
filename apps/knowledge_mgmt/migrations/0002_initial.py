# Generated by Django 4.2.7 on 2024-10-10 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("model_provider_mgmt", "0001_initial"),
        ("knowledge_mgmt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="knowledgedocument",
            name="ocr_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="model_provider_mgmt.ocrprovider",
                verbose_name="OCR model",
            ),
        ),
        migrations.AddField(
            model_name="knowledgedocument",
            name="semantic_chunk_parse_embedding_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="model_provider_mgmt.embedprovider",
                verbose_name="embedding model",
            ),
        ),
        migrations.AddField(
            model_name="knowledgebase",
            name="embed_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="model_provider_mgmt.embedprovider",
                verbose_name="Embed Model",
            ),
        ),
        migrations.AddField(
            model_name="knowledgebase",
            name="rerank_model",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="model_provider_mgmt.rerankprovider",
                verbose_name="Rerank Model",
            ),
        ),
        migrations.AddField(
            model_name="fileknowledge",
            name="knowledge_document",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="knowledge_mgmt.knowledgedocument",
                verbose_name="Knowledge Document",
            ),
        ),
    ]
