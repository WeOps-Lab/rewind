from rest_framework import routers

from apps.base.quota_rule_mgmt.views import QuotaRuleViewSet
from apps.base.user_api_secret_mgmt.views import UserAPISecretViewSet

router = routers.DefaultRouter()
urlpatterns = []
router.register(r"user_api_secret", UserAPISecretViewSet)
router.register(r"quota_rule", QuotaRuleViewSet)

urlpatterns += router.urls
