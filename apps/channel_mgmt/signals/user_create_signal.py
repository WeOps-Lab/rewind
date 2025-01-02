from apps.base.models import User
from apps.channel_mgmt.services.channel_init_service import ChannelInitService


def user_create_signal(**kwargs):
    user, _ = User.objects.get_or_create(username="admin", defaults={"is_superuser": True, "is_staff": True})
    service = ChannelInitService(owner=user)
    service.init()
