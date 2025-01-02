from apps.base.models import User
from apps.bot_mgmt.services.bot_init_service import BotInitService


def user_create_signal(**kwargs):
    user, _ = User.objects.get_or_create(username="admin", defaults={"is_superuser": True, "is_staff": True})
    service = BotInitService(owner=user)
    service.init()
