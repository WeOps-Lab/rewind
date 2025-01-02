from apps.base.models import User
from apps.model_provider_mgmt.services.model_provider_init_service import ModelProviderInitService


def user_create_signal(**kwargs):
    user, _ = User.objects.get_or_create(username="admin", defaults={"is_superuser": True, "is_staff": True})
    service = ModelProviderInitService(owner=user)
    service.init()
