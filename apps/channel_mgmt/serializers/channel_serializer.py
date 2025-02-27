from apps.channel_mgmt.models import Channel, ChannelTemplate
from config.drf.serializers import I18nSerializer


class ChannelSerializer(I18nSerializer):
    class Meta:
        model = Channel
        fields = "__all__"


class ChannelTemplateSerializer(I18nSerializer):
    class Meta:
        model = ChannelTemplate
        fields = "__all__"
