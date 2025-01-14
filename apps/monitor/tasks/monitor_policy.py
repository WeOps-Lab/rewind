import logging
import uuid

from celery.app import shared_task
from datetime import datetime, timezone

from django.conf.global_settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail

from apps.core.utils.keycloak_client import KeyCloakClient
from apps.monitor.constants import THRESHOLD_METHODS, LEVEL_WEIGHT, MONITOR_OBJS
from apps.monitor.models import MonitorPolicy, MonitorInstanceOrganization, MonitorAlert, MonitorEvent, MonitorInstance
from apps.monitor.utils.victoriametrics_api import VictoriaMetricsAPI

logger = logging.getLogger("app")


@shared_task
def scan_policy_task(policy_id):
    """扫描监控策略"""
    logger.info("start to update monitor instance grouping rule")

    policy_obj = MonitorPolicy.objects.filter(id=policy_id).select_related("metric", "monitor_object").first()
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

    def for_mat_period(self):
        """格式化周期"""
        if not self.policy.period:
            raise ValueError("policy period is empty")
        if self.policy.period["type"] == "min":
            return f'{self.policy.period["value"]}{"m"}'
        elif self.policy.period["type"] == "hour":
            return f'{self.policy.period["value"]}{"h"}'
        elif self.policy.period["type"] == "day":
            return f'{self.policy.period["value"]}{"d"}'
        else:
            raise ValueError(f"invalid period type: {self.policy.period['type']}")

    def period_to_seconds(self):
        """周期转换为秒"""
        if not self.policy.period:
            raise ValueError("policy period is empty")
        if self.policy.period["type"] == "min":
            return self.policy.period["value"] * 60
        elif self.policy.period["type"] == "hour":
            return self.policy.period["value"] * 3600
        elif self.policy.period["type"] == "day":
            return self.policy.period["value"] * 86400
        else:
            raise ValueError(f"invalid period type: {self.policy.period['type']}")

    def query_aggregration_metrics(self):
        """查询指标"""
        end_timestamp = int(datetime.now(timezone.utc).timestamp())
        period_seconds = self.period_to_seconds()
        start_timestamp = end_timestamp - period_seconds
        query = self.policy.metric.query
        # 实例条件
        instances_str = "|".join(self.instances_map.keys())
        instance_str = f"instance_id=~'{instances_str}'," if instances_str else ""
        # 纬度条件
        vm_filter_str = self.format_to_vm_filter(self.policy.filter)
        vm_filter_str = f"{vm_filter_str}" if vm_filter_str else ""
        label_str = f"{instance_str}{vm_filter_str}"
        # 去掉label尾部多余的逗号
        if label_str.endswith(","):
            label_str = label_str[:-1]
        query = query.replace("__$labels__", label_str)
        step = self.for_mat_period()
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
            value = metric_info["values"][-1]
            result[instance_id] = float(value[1])
        return result

    def compare_event(self, aggregation_result):
        """比较事件"""
        compare_result = []

        # 计算无数据事件
        for instance_id in self.instances_map.keys():
            if instance_id not in aggregation_result:
                compare_result.append({
                    "instance_id": instance_id,
                    "value": None,
                    "level": "no_data",
                    "content": "no data",
                })

        # 计算告警事件
        for instance_id, value in aggregation_result.items():

            event = None
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
                    break

            # 未触发阈值的事件
            if not event:
                event = {
                    "instance_id": instance_id,
                    "value": value,
                    "level": "info",
                    "content": "",
                }

            compare_result.append(event)

        return compare_result

    def create_event(self, events):
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
        client = KeyCloakClient()
        users = client.realm_client.get_users()
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

    def recovery_alert(self, event_objs):
        """告警恢复处理"""
        if self.policy.recovery_condition <= 0:
            return
        event_objs_map = {event.monitor_instance_id: event for event in event_objs}
        recovery_alerts, alert_level_updates = [], []
        for alert in self.active_alerts:
            event_obj = event_objs_map.get(alert.monitor_instance_id)
            if not event_obj:
                continue
            if alert.alert_type == "no_data":
                # 无数据告警恢复
                if event_obj.level != "no_data":
                    alert.status = "recovered"
                    alert.end_event_time = event_obj.created_at
                    alert.operator = "system"
                    recovery_alerts.append(alert)
            else:
                if event_obj.level == "no_data":
                    continue
                # 正常告警恢复
                if event_obj.level == "info":
                    events = MonitorEvent.objects.filter(
                        policy_id=self.policy.id,
                        monitor_instance_id=event_obj.monitor_instance_id,
                    ).order_by("-created_at")[:self.policy.recovery_condition]
                    if all(event.level == "info" for event in events):
                        alert.status = "recovered"
                        alert.end_event_time = event_obj.created_at
                        alert.operator = "system"
                        recovery_alerts.append(alert)
                else:
                    # 告警等级升级
                    new_level = event_obj.level
                    old_level = alert.level
                    if LEVEL_WEIGHT.get(new_level) > LEVEL_WEIGHT.get(old_level):
                        alert.level = new_level
                        alert.value = event_obj.value
                        alert.content = event_obj.content
                        alert_level_updates.append(alert)
        if alert_level_updates:
            MonitorAlert.objects.bulk_update(alert_level_updates, ["level", "value", "content"], batch_size=200)
        if recovery_alerts:
            MonitorAlert.objects.bulk_update(recovery_alerts, ["status", "end_event_time", "operator"], batch_size=200)

    def create_alert(self, event_objs):
        """告警生成处理"""
        no_data_events, alert_events = [], []
        for event_obj in event_objs:
            if event_obj.level == "info":
                continue
            if event_obj.level == "no_data":
                if self.policy.no_data_alert <= 0:
                    continue
                no_data_events.append(event_obj)
            else:
                alert_events.append(event_obj)

        # 正常告警
        alert_objs = [
            MonitorAlert(
                policy_id=self.policy.id,
                monitor_instance_id=event_obj.monitor_instance_id,
                alert_type="alert",
                level=event_obj.level,
                value=event_obj.value,
                content=event_obj.content,
                status="new",
                start_event_time=event_obj.created_at,
                operator="",
            )
            for event_obj in alert_events
        ]

        # 无数据告警
        for event_obj in no_data_events:
            events = MonitorEvent.objects.filter(
                policy_id=self.policy.id,
                monitor_instance_id=event_obj.monitor_instance_id,
            ).order_by("-created_at")[:self.policy.no_data_alert]
            if all(event.level == "no_data" for event in events):
                alert_objs.append(
                    MonitorAlert(
                        policy_id=self.policy.id,
                        monitor_instance_id=event_obj.monitor_instance_id,
                        alert_type="no_data",
                        level=self.policy.no_data_level,
                        value=None,
                        content="no data",
                        status="new",
                        start_event_time=event_obj.created_at,
                        operator="system",
                    )
                )
        MonitorAlert.objects.bulk_create(alert_objs, batch_size=200)

    def alert_handling(self, event_objs):
        """告警处理"""

        active_alert_map = {alert.monitor_instance_id for alert in self.active_alerts}
        recovery_alert_events, create_alert_events = [], []
        for event_obj in event_objs:
            if event_obj.monitor_instance_id in active_alert_map:
                recovery_alert_events.append(event_obj)
            else:
                create_alert_events.append(event_obj)

        # 告警恢复处理
        self.recovery_alert(recovery_alert_events)

        # 告警生成处理
        self.create_alert(create_alert_events)

    def run(self):
        """运行"""
        self.set_monitor_obj_instance_key()
        aggregration_metrics = self.query_aggregration_metrics()
        aggregation_result = self.format_aggregration_metrics(aggregration_metrics)
        events = self.compare_event(aggregation_result)
        event_objs = self.create_event(events)
        self.alert_handling(event_objs)
        self.notice(event_objs)
