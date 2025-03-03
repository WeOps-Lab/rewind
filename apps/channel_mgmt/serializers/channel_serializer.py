from apps.channel_mgmt.models import Channel, ChannelTemplate
from config.drf.serializers import I18nSerializer


class ChannelSerializer(I18nSerializer):
    class Meta:
        model = Channel
        fields = "__all__"

    def create(self, validated_data):
        if validated_data["channel_type"] == "email":
            validated_data["config"] = {
                "smtp_server": "",
                "port": 0,
                "smtp_user": "",
                "smtp_pwd": "",
                "smtp_usessl": False,
                "smtp_usetls": False,
                "mail_sender": "",
            }
        else:
            validated_data["config"] = {
                "corp_id": "",
                "secret": "",
                "token": "",
                "aes_key": "",
                "agent_id": "",
            }
        return super().create(validated_data)


class ChannelTemplateSerializer(I18nSerializer):
    class Meta:
        model = ChannelTemplate
        fields = "__all__"
