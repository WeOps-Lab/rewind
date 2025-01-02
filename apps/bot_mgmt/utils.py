import datetime


def set_time_range(end_time_str, start_time_str):
    today = datetime.datetime.today()
    # 解析时间字符串到 datetime 对象，并处理空值
    if start_time_str:
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        start_time = today.replace(hour=0, minute=0, second=0, microsecond=0)
    if end_time_str:
        end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    else:
        end_time = today.replace(hour=23, minute=59, second=59, microsecond=999999)
    return end_time, start_time
