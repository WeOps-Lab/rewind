from apps.node_mgmt.models.sidecar import Collector


COLLECTORS = [
    {
        "id": "telegraf_linux",
        "name": "telegraf",
        "node_operating_system": "linux",
        "service_type": "svc",
        "executable_path": "/opt/fusion-collectors/bin/telegraf",
        "execute_parameters": "-config %s",
        "validation_parameters": "-test -config /etc/telegraf/telegraf.conf",
        "default_template": "",
        "introduction": "Telegraf 是一个插件驱动的服务器代理，用于收集和报告指标。"
    },
    {
        "id": "telegraf_windows",
        "name": "telegraf",
        "node_operating_system": "windows",
        "service_type": "svc",
        "executable_path": "C:\\Program Files\\Telegraf\\telegraf.exe",
        "execute_parameters": "-config C:\\Program Files\\Telegraf\\telegraf.conf",
        "validation_parameters": "-test -config C:\\Program Files\\Telegraf\\telegraf.conf",
        "default_template": "",
        "introduction": "Telegraf 是一个插件驱动的服务器代理，用于收集和报告指标。"
    },
]


def collector_init():
    """
    初始化采集器
    """
    old_collector = Collector.objects.all()
    old_collector_set = {i.id for i in old_collector}

    create_collectors, update_collectors = [], []

    for collector_info in COLLECTORS:
        if collector_info["id"] in old_collector_set:
            update_collectors.append(collector_info)
        else:
            create_collectors.append(collector_info)

    if create_collectors:
        Collector.objects.bulk_create([Collector(**i) for i in create_collectors])

    if update_collectors:
        Collector.objects.bulk_update([Collector(**i) for i in update_collectors], ["service_type", "executable_path", "execute_parameters", "validation_parameters", "default_template", "introduction"])
