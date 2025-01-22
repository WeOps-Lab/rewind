import logging
import uuid

from celery.app import shared_task
from datetime import datetime, timezone

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from apps.monitor.constants import THRESHOLD_METHODS, LEVEL_WEIGHT, MONITOR_OBJS
from apps.monitor.models import MonitorPolicy, MonitorInstanceOrganization, MonitorAlert, MonitorEvent, MonitorInstance, \
    Metric
from apps.monitor.utils.system_mgmt_api import SystemMgmtUtils
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI

logger = logging.getLogger("app")


@shared_task
def scan_policy_task(policy_id):
    """扫描监控策略"""
    logger.info("start to update monitor instance grouping rule")

    policy_obj = MonitorPolicy.objects.filter(id=policy_id).select_related("monitor_object").first()
    if not policy_obj:
        raise ValueError(f"No MonitorPolicy found with id {policy_id}")

    if policy_obj.enable:
        policy_obj.last_run_time = datetime.now(timezone.utc)           # 更新最后执行时间
        policy_obj.save()
        MonitorPolicyScan(policy_obj).run()                        # 执行监控策略

    logger.info("end to update monitor instance grouping rule")


def new_value(metric_query, start, end, step, group_by):
    query = f"any(last_over_time({metric_query})) by ({group_by})"
    metrics = VictoriaMetricsAPI().query_range(query, start, end, step)
    return metrics


def max_value(metric_query, start, end, step, group_by):
    query = f"any(max_over_time({metric_query})) by ({group_by})"
    metrics = VictoriaMetricsAPI().query_range(query, start, end, step)
    return metrics


def min_value(metric_query, start, end, step, group_by):
    query = f"any(min_over_time({metric_query})) by ({group_by})"
    metrics = VictoriaMetricsAPI().query_range(query, start, end, step)
    return metrics


def avg_value(metric_query, start, end, step, group_by):
    query = f"any(avg_over_time({metric_query})) by ({group_by})"
    metrics = VictoriaMetricsAPI().query_range(query, start, end, step)
    return metrics


def sum_value(metric_query, start, end, step, group_by):
    query = f"any(sum_over_time({metric_query})) by ({group_by})"
    metrics = VictoriaMetricsAPI().query_range(query, start, end, step)
    return metrics


METHOD = {
    "sum": sum_value,
    "avg": avg_value,
    "max": max_value,
    "min": min_value,
    "new": new_value,
}


class MonitorPolicyScan:
    def __init__(self, policy):
        self.policy = policy
        self.instances_map = self.instances_map()
        self.active_alerts = self.get_active_alerts()
        self.instance_id_key = None

    def get_active_alerts(self):
        """获取策略的活动告警"""
        return MonitorAlert.objects.filter(policy_id=self.policy.id, status="new")

    def instances_map(self):
        """获取策略适用的实例"""
        source_type, source_values = self.policy.source["type"], self.policy.source["values"]
        if source_type == "instance":
            instance_list = source_values
        elif source_type == "organization":
            instance_list = list(MonitorInstanceOrganization.objects.filter(organization__in=source_values).values_list(
                "monitor_instance_id", flat=True
            ))
        else:
            instance_list = []
        objs = MonitorInstance.objects.filter(id__in=instance_list)
        return {i.id: i.name for i in objs}

    def format_to_vm_filter(self, conditions):
        """
        将纬度条件格式化为 VictoriaMetrics 的标准语法。

        Args:
            conditions (list): 包含过滤条件的字典列表，每个字典格式为：
                {"name": <纬度名称>, "value": <值>, "method": <运算符>}

        Returns:
            str: 格式化后的 VictoriaMetrics 过滤条件语法。
        """
        vm_filters = []
        for condition in conditions:
            name = condition.get("name")
            value = condition.get("value")
            method = condition.get("method")
            vm_filters.append(f'{name}{method}"{value}"')

        # 使用逗号连接多个条件
        return ",".join(vm_filters)

    def for_mat_period(self, period, points=1):
        """格式化周期"""
        if not period:
            raise ValueError("policy period is empty")
        if period["type"] == "min":
            return f'{int(period["value"]/points)}{"m"}'
        elif period["type"] == "hour":
            return f'{int(period["value"]/points)}{"h"}'
        elif period["type"] == "day":
            return f'{int(period["value"]/points)}{"d"}'
        else:
            raise ValueError(f"invalid period type: {period['type']}")

    def period_to_seconds(self, period):
        """周期转换为秒"""
        if not period:
            raise ValueError("policy period is empty")
        if period["type"] == "min":
            return period["value"] * 60
        elif period["type"] == "hour":
            return period["value"] * 3600
        elif period["type"] == "day":
            return period["value"] * 86400
        else:
            raise ValueError(f"invalid period type: {period['type']}")

    def format_pmq(self):
        """格式化PMQ"""

        query_condition = self.policy.query_condition
        _type = query_condition.get("type")
        if type == "pmq":
            return query_condition.get("query")
        else:
            metric_id = query_condition.get("metric_id")
            metric_obj = Metric.objects.filter(id=metric_id).first()
            query = metric_obj.query
            # 纬度条件
            _filter = query_condition.get("filter", [])
            vm_filter_str = self.format_to_vm_filter(_filter)
            vm_filter_str = f"{vm_filter_str}" if vm_filter_str else ""
            # 去掉label尾部多余的逗号
            if vm_filter_str.endswith(","):
                vm_filter_str = vm_filter_str[:-1]
            query = query.replace("__$labels__", vm_filter_str)
            return query

    def query_aggregration_metrics(self, period, points=1):
        """查询指标"""
        end_timestamp = int(datetime.now(timezone.utc).timestamp())
        period_seconds = self.period_to_seconds(period)
        start_timestamp = end_timestamp - period_seconds

        query = self.format_pmq()

        step = self.for_mat_period(period, points)
        method = METHOD.get(self.policy.algorithm)
        if not method:
            raise ValueError("invalid algorithm method")
        return method(query, start_timestamp, end_timestamp, step, ",".join(self.policy.group_by))

    def set_monitor_obj_instance_key(self):
        """获取监控对象实例key"""
        for monitor_obj in MONITOR_OBJS:
            if monitor_obj["name"] == self.policy.monitor_object.name:
                self.instance_id_key= monitor_obj["instance_id_key"]
                break
        if not self.instance_id_key:
            raise ValueError("invalid monitor object instance key")

    def format_aggregration_metrics(self, metrics):
        """格式化聚合指标"""
        result = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = metric_info["metric"].get(self.instance_id_key)
            # 过滤不在实例列表中的实例（策略实例范围）
            if self.instances_map and instance_id not in self.instances_map:
                continue
            value = metric_info["values"][-1]
            result[instance_id] = float(value[1])
        return result

    def format_aggregration_metrics_v2(self, metrics, value_points=1):
        """格式化聚合指标"""
        result = {}
        for metric_info in metrics.get("data", {}).get("result", []):
            instance_id = metric_info["metric"].get(self.instance_id_key)
            # 过滤不在实例列表中的实例（策略实例范围）
            if self.instances_map and instance_id not in self.instances_map:
                continue
            values = metric_info["values"][-value_points:]
            result[instance_id] = [float(value) for value in values]
        return result

    def alert_event(self):
        """告警事件"""
        aggregration_metrics = self.query_aggregration_metrics(self.policy.period)
        aggregation_result = self.format_aggregration_metrics(aggregration_metrics)
        events = []

        # 计算告警事件
        for instance_id, value in aggregation_result.items():
            for threshold_info in self.policy.threshold:
                method = THRESHOLD_METHODS.get(threshold_info["method"])
                if not method:
                    raise ValueError("invalid threshold method")
                if method(value, threshold_info["value"]):
                    event = {
                        "instance_id": instance_id,
                        "value": value,
                        "level": threshold_info["level"],
                        "content": f'{self.policy.monitor_object.type}-{self.policy.monitor_object.name} {self.instances_map.get(instance_id, "")} {self.policy.metric.display_name} {threshold_info["method"]} {threshold_info["value"]}',
                    }
                    events.append(event)
                    break

        return events

    def no_data_event(self):
        """无数据告警事件"""
        if not self.policy.no_data_period:
            return []

        events = []
        _aggregration_metrics = self.query_aggregration_metrics(self.policy.no_data_period)
        _aggregation_result = self.format_aggregration_metrics(_aggregration_metrics)

        # 计算无数据事件
        for instance_id in self.instances_map.keys():
            if instance_id not in _aggregation_result:
                events.append({
                    "instance_id": instance_id,
                    "value": None,
                    "level": "no_data",
                    "content": "no data",
                })

        return events

    def recovery_alert(self):
        """告警恢复"""
        if self.policy.recovery_condition <= 0:
            return
        _period = {
            "type": self.policy.period["type"],
            "value": self.policy.period["value"] * self.policy.recovery_condition
        }
        _aggregration_metrics = self.query_aggregration_metrics(_period, self.policy.recovery_condition)
        _aggregation_result = self.format_aggregration_metrics_v2(_aggregration_metrics, self.policy.recovery_condition)

        recovery_alert_instance_ids = []

        active_alert_instance_ids = {alert.monitor_instance_id for alert in self.active_alerts}
        for instance_id, values in _aggregation_result.items():
            if instance_id not in active_alert_instance_ids:
                continue
            # 都是info级别，告警恢复
            is_info = True
            for value in values:
                for threshold_info in self.policy.threshold:
                    method = THRESHOLD_METHODS.get(threshold_info["method"])
                    if not method:
                        raise ValueError("invalid threshold method")
                    if method(value, threshold_info["value"]):
                        is_info = False
                        break
            if is_info:
                recovery_alert_instance_ids.append(instance_id)

        MonitorAlert.objects.filter(
            policy_id=self.policy.id,
            monitor_instance_id__in=recovery_alert_instance_ids,
            status="new",
        ).update(status="recovered", end_event_time=datetime.now(timezone.utc), operator="system")

    def recovery_no_data_alert(self):
        """无数据告警恢复"""
        if not self.policy.no_data_recovery_period:
            return
        _aggregration_metrics = self.query_aggregration_metrics(self.policy.no_data_recovery_period)
        _aggregation_result = self.format_aggregration_metrics(_aggregration_metrics)
        instance_ids = set(_aggregation_result.keys())
        MonitorAlert.objects.filter(
            policy_id=self.policy.id,
            monitor_instance_id__in=instance_ids,
            alert_type="no_data",
            status="new",
        ).update(status="recovered", end_event_time=datetime.now(timezone.utc), operator="system")

    def create_events(self, events):
        """创建事件"""
        new_event_creates = [
            MonitorEvent(
                id=uuid.uuid4().hex,
                policy_id=self.policy.id,
                monitor_instance_id=event["instance_id"],
                value=event["value"],
                level=event["level"],
                content=event["content"],
                notice_result=True,
            )
            for event in events
        ]
        event_objs = MonitorEvent.objects.bulk_create(new_event_creates, batch_size=200)
        return event_objs

    def get_users_email(self, usernames):
        """获取用户邮箱"""
        users = SystemMgmtUtils.get_user_all()
        user_email_map = {user_info["username"]: user_info["email"] for user_info in users if user_info.get("email")}

        return {username: user_email_map.get(username) for username in usernames}

    def send_email(self, event_obj):
        """发送邮件"""
        title = f"告警通知：{self.policy.name}"
        content = f"告警内容：{event_obj.content}"
        result = []
        user_email_map = self.get_users_email(self.policy.notice_users)

        for user, email in user_email_map.items():
            if not email:
                result.append({"user": user, "status": "failed", "error": "email not found"})
                continue
            else:
                result.append({"user": user, "status": "success"})

        try:
            send_mail(
                subject=title,
                message=content,
                from_email=DEFAULT_FROM_EMAIL,
                recipient_list=[email for email in user_email_map.values() if email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(f"send email failed: {e}")

        return result

    def notice(self, event_objs):
        """通知"""
        active_alert_set = {alert.monitor_instance_id for alert in self.active_alerts}
        for event in event_objs:
            # 非异常事件不通知
            if event.level == "info":
                continue
            if event.level == "no_data":
                # 无数据告警通知为开启，不进行通知
                if self.policy.no_data_alert <= 0:
                    continue
                # 没有活跃告警，不进行通知
                if event.monitor_instance_id not in active_alert_set:
                    continue
            notice_results = self.send_email(event)
            event.notice_result = notice_results
        # 批量更新通知结果
        MonitorEvent.objects.bulk_update(event_objs, ["notice_result"], batch_size=200)

    def handle_alert_events(self, event_objs):
        """处理告警事件"""
        new_alert_events, old_alert_events = [], []
        instance_ids = {event.monitor_instance_id for event in self.active_alerts}
        for event_obj in event_objs:
            if event_obj.monitor_instance_id in instance_ids:
                old_alert_events.append(event_obj)
            else:
                new_alert_events.append(event_obj)

        self.update_alert(old_alert_events)
        self.create_alert(new_alert_events)


    def update_alert(self, event_objs):
        event_map = {event.monitor_instance_id: event for event in event_objs}
        alert_level_updates = []
        for alert in self.active_alerts:
            event_obj = event_map.get(alert.monitor_instance_id)
            if not event_obj or event_obj.level == "no_data":
                continue
            # 告警等级升级
            if LEVEL_WEIGHT.get(event_obj.level) > LEVEL_WEIGHT.get(alert.level):
                alert.level = event_obj.level
                alert.value = event_obj.value
                alert.content = event_obj.content
                alert_level_updates.append(alert)
        MonitorAlert.objects.bulk_update(alert_level_updates, ["level", "value", "content"], batch_size=200)

    def create_alert(self, event_objs):
        """告警生成处理"""
        create_alerts = []
        for event_obj in event_objs:
            if event_obj.level == "no_data":
                alert_type = "alert"
                level = event_obj.level,
                value = event_obj.value,
                content = event_obj.content,
            else:
                alert_type = "no_data"
                level = self.policy.no_data_level,
                value = None,
                content = "no data",
            create_alerts.append(
                MonitorAlert(
                    policy_id=self.policy.id,
                    monitor_instance_id=event_obj.monitor_instance_id,
                    alert_type=alert_type,
                    level=level,
                    value=value,
                    content=content,
                    status="new",
                    start_event_time=event_obj.created_at,
                    operator="",
                ))

        MonitorAlert.objects.bulk_create(create_alerts, batch_size=200)

    def run(self):
        """运行"""
        self.set_monitor_obj_instance_key()

        # 告警事件
        alert_events =  self.alert_event()
        # 无数据事件
        no_data_events = self.no_data_event()
        # 告警恢复
        self.recovery_alert()
        # 无数据告警恢复
        self.recovery_no_data_alert()

        # 告警事件记录
        event_objs = self.create_events(alert_events + no_data_events)
        self.handle_alert_events(event_objs)
        self.notice(event_objs)
