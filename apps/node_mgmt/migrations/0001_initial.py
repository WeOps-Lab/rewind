# Generated by Django 4.2.7 on 2025-01-07 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CloudRegion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='云区域名称')),
                ('introduction', models.TextField(blank=True, verbose_name='云区域介绍')),
            ],
            options={
                'verbose_name': '云区域',
                'verbose_name_plural': '云区域',
                'db_table': 'cloud_region',
            },
        ),
        migrations.CreateModel(
            name='Collector',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='采集器ID')),
                ('name', models.CharField(max_length=100, verbose_name='采集器名称')),
                ('service_type', models.CharField(choices=[('exec', '执行任务'), ('svc', '服务')], max_length=100, verbose_name='服务类型')),
                ('node_operating_system', models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows')], max_length=50, verbose_name='节点操作系统类型')),
                ('executable_path', models.CharField(max_length=200, verbose_name='可执行文件路径')),
                ('execute_parameters', models.CharField(max_length=200, verbose_name='执行参数')),
                ('validation_parameters', models.CharField(blank=True, max_length=200, null=True, verbose_name='验证参数')),
                ('default_template', models.TextField(blank=True, null=True, verbose_name='默认模板')),
                ('introduction', models.TextField(blank=True, verbose_name='采集器介绍')),
            ],
            options={
                'verbose_name': '采集器信息',
                'verbose_name_plural': '采集器信息',
                'db_table': 'collector',
            },
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='节点ID')),
                ('name', models.CharField(max_length=100, verbose_name='节点名称')),
                ('ip', models.CharField(max_length=30, verbose_name='IP地址')),
                ('operating_system', models.CharField(choices=[('linux', 'Linux'), ('windows', 'Windows')], max_length=50, verbose_name='操作系统类型')),
                ('collector_configuration_directory', models.CharField(max_length=200, verbose_name='采集器配置目录')),
                ('metrics', models.JSONField(default=dict, verbose_name='指标')),
                ('status', models.JSONField(default=dict, verbose_name='状态')),
                ('tags', models.JSONField(default=list, verbose_name='标签')),
                ('log_file_list', models.JSONField(default=list, verbose_name='日志文件列表')),
                ('cloud_region', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.cloudregion', verbose_name='云区域')),
            ],
            options={
                'verbose_name': '节点信息',
                'verbose_name_plural': '节点信息',
                'db_table': 'node',
            },
        ),
        migrations.CreateModel(
            name='SidecarApiToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('token', models.CharField(max_length=100, verbose_name='Token')),
            ],
            options={
                'verbose_name': 'Sidecar API Token',
                'verbose_name_plural': 'Sidecar API Token',
                'db_table': 'sidecar_api_token',
            },
        ),
        migrations.CreateModel(
            name='CollectorConfiguration',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='配置ID')),
                ('name', models.CharField(max_length=100, verbose_name='配置名称')),
                ('config_template', models.TextField(blank=True, verbose_name='配置模板')),
                ('cloud_region', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.cloudregion', verbose_name='云区域')),
                ('collector', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.collector', verbose_name='采集器')),
                ('nodes', models.ManyToManyField(blank=True, to='node_mgmt.node', verbose_name='节点')),
            ],
            options={
                'verbose_name': '采集器配置信息',
                'verbose_name_plural': '采集器配置信息',
                'db_table': 'collector_configuration',
            },
        ),
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('action', models.JSONField(default=list, verbose_name='操作')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.node', verbose_name='节点')),
            ],
            options={
                'verbose_name': '操作信息',
                'verbose_name_plural': '操作信息',
                'db_table': 'action',
            },
        ),
        migrations.CreateModel(
            name='SidecarEnv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, verbose_name='描述')),
                ('cloud_region', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.cloudregion', verbose_name='云区域')),
            ],
            options={
                'verbose_name': 'Sidecar环境变量',
                'verbose_name_plural': 'Sidecar环境变量',
                'db_table': 'sidecar_env',
                'unique_together': {('key', 'cloud_region')},
            },
        ),
        migrations.CreateModel(
            name='NodeOrganization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Created Time')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Time')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='Creator')),
                ('updated_by', models.CharField(default='', max_length=32, verbose_name='Updater')),
                ('organization', models.CharField(max_length=100, verbose_name='组织id')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='node_mgmt.node', verbose_name='节点')),
            ],
            options={
                'verbose_name': '节点组织',
                'verbose_name_plural': '节点组织',
                'db_table': 'node_organization',
                'unique_together': {('node', 'organization')},
            },
        ),
    ]
