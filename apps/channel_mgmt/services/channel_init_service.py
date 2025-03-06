# from apps.channel_mgmt.models import ChannelChoices, ChannelTemplate
from apps.core.logger import logger


class ChannelInitService:
    def __init__(self, owner):
        self.owner = owner.username

    @staticmethod
    def init():
        logger.info("初始化监控告警模板")


#         ChannelTemplate.objects.get_or_create(
#             name="Alarm Notification",
#             channel_type=ChannelChoices.ENTERPRISE_WECHAT,
#             app="monitor",
#             defaults={
#                 "title": "${status}: 【${level}】${bk_biz_name}${bk_obj_name}${object}${item}",
#                 "context": """告警时间： ${alarm_time}
# 告警对象: ${object}
# 告警指标: ${item}
# 告警内容: ${content}
# 告警状态: ${status}
# 对象类型: ${bk_obj_name}
# 所属应用: ${bk_biz_name}
# 告警维度: ${dimension}
# 告警来源: ${source_name}
# """
#             },
#         )
