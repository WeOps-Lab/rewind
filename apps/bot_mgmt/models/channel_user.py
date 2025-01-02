from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.channel_mgmt.models import ChannelChoices


class ChannelUser(models.Model):
    user_id = models.CharField(max_length=100, verbose_name="用户ID")
    name = models.CharField(max_length=100, verbose_name="名称", blank=True, null=True)
    channel_type = models.CharField(max_length=100, choices=ChannelChoices.choices, verbose_name=_("channel type"))

    class Meta:
        verbose_name = "消息通道用户"
        verbose_name_plural = verbose_name

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "channel_type": self.channel_type,
            "channel_type_display": self.get_channel_type_display(),
        }
