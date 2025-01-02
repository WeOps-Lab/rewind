from django.db import models
from django.utils.translation import gettext_lazy as _
from django_yaml_field import YAMLField

from apps.core.mixinx import EncryptMixin
from apps.core.models.maintainer_info import MaintainerInfo


class ChannelChoices(models.TextChoices):
    ENTERPRISE_WECHAT = ("enterprise_wechat", _("Enterprise WeChat"))
    ENTERPRISE_WECHAT_BOT = ("enterprise_wechat_bot", _("Enterprise WeChat Bot"))
    WECHAT_OFFICIAL_ACCOUNT = ("wechat_official_account", _("WeChat Official Account"))
    DING_TALK = ("ding_talk", _("Ding Talk"))
    WEB = ("web", _("Web"))
    GITLAB = ("gitlab", _("GitLab"))


class Channel(MaintainerInfo, EncryptMixin):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    channel_type = models.CharField(max_length=100, choices=ChannelChoices.choices, verbose_name=_("channel type"))
    channel_config = YAMLField(verbose_name=_("channel config"), blank=True, null=True)
    enabled = models.BooleanField(default=False, verbose_name=_("enabled"))

    class Meta:
        verbose_name = _("channel")
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
