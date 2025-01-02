from apps.bot_mgmt.models import Bot
from config.drf.serializers import TeamSerializer


class BotSerializer(TeamSerializer):
    class Meta:
        model = Bot
        fields = "__all__"
