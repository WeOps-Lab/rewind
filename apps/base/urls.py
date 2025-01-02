from rest_framework import routers

from apps.base.user_api_secret_mgmt.views import UserAPISecretViewSet

router = routers.DefaultRouter()
urlpatterns = []
router.register(r"user_api_secret", UserAPISecretViewSet)

urlpatterns += router.urls
