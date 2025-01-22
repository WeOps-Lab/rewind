# Generated by Django 4.2.7 on 2025-01-22 09:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_monitorpolicy_collect_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitorpolicy',
            name='alert_name',
            field=models.CharField(default='', max_length=200, verbose_name='告警名称'),
        ),
        migrations.CreateModel(
            name='MonitorEventRawData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.JSONField(default=dict, verbose_name='原始数据')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.monitorevent', verbose_name='事件')),
            ],
        ),
    ]
