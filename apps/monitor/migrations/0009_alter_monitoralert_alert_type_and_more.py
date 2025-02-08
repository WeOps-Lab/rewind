# Generated by Django 4.2.7 on 2025-02-08 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0008_monitoralert_info_event_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitoralert',
            name='alert_type',
            field=models.CharField(choices=[('alert', 'Alert'), ('no_data', 'No Data')], db_index=True, default='alert', max_length=50, verbose_name='告警类型'),
        ),
        migrations.AlterField(
            model_name='monitoralert',
            name='level',
            field=models.CharField(db_index=True, default='', max_length=20, verbose_name='最高告警级别'),
        ),
        migrations.AddIndex(
            model_name='monitorevent',
            index=models.Index(fields=['policy_id', 'monitor_instance_id', 'created_at'], name='monitor_mon_policy__62dd7f_idx'),
        ),
    ]
