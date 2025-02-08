import pandas as pd
from string import Template

from apps.monitor.constants import THRESHOLD_METHODS


def vm_to_dataframe(vm_data, instance_id_keys=None):
    """将 VM 数据转换为 DataFrame，支持多维度组合 _instance_id"""
    df = pd.json_normalize(vm_data)  # 展开 metric 字段

    # 获取所有 metric 维度
    metric_cols = [col for col in df.columns if col.startswith("metric.")]

    # 选择用于拼接 _instance_id 的维度字段
    if instance_id_keys:
        selected_cols = [f"metric.{key}" for key in instance_id_keys if f"metric.{key}" in metric_cols]
    else:
        selected_cols = ["metric.instance_id"]  # 默认使用 instance_id

    # 生成 _instance_id（拼接选定的维度字段）
    df["_instance_id"] = df[selected_cols].astype(str).agg("_".join, axis=1)

    return df[["_instance_id", "values"]]  # 只保留关键信息



def calculate_alerts(alert_name, df, thresholds, n=1):
    """计算告警事件"""
    alert_events, info_events = [], []

    # 遍历每一行数据（每个 _instance_id）
    for _, row in df.iterrows():
        _instance_id = row["_instance_id"]

        # 取最近 n 个数据点，保证窗口长度为 n
        values = row["values"][-n:]
        if len(values) < n:
            continue

        raw_data = row.to_dict()
        raw_data["values"] = values
        # 计算该窗口是否满足阈值
        alert_triggered = False
        for threshold_info in thresholds:
            method = THRESHOLD_METHODS.get(threshold_info["method"])
            if not method:
                raise ValueError(f"Invalid threshold method: {threshold_info['method']}")

            # 解析值并检查是否满足阈值
            if all(method(float(v[1]), threshold_info["value"]) for v in values):
                # 生成告警事件
                template = Template(alert_name)
                content = template.safe_substitute(raw_data)

                event = {
                    "instance_id": _instance_id,
                    "value": values[-1][1],  # 最后一个时间点的值
                    "timestamp": values[-1][0],  # 最后一个时间点的时间戳
                    "level": threshold_info["level"],
                    "content": content,
                    "raw_data": raw_data,  # 记录最近 n 个匹配的原始数据
                }
                alert_events.append(event)
                alert_triggered = True
                break  # 一旦匹配，跳出阈值循环

        if not alert_triggered:
            # 记录 info 事件
            info_events.append({
                "instance_id": _instance_id,
                "value": values[-1][1],
                "timestamp": values[-1][0],
                "level": "info",
                "content": "info",
            })

    return alert_events, info_events