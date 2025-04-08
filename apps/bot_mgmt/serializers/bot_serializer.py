from apps.bot_mgmt.models import Bot
from config.drf.serializers import AuthSerializer, TeamSerializer


class BotSerializer(TeamSerializer, AuthSerializer):
    permission_key = "bot"

    class Meta:
        model = Bot
        fields = "__all__"
