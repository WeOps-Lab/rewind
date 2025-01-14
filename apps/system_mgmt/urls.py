from rest_framework import routers

from apps.system_mgmt.viewset import GroupViewSet, RoleViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"group", GroupViewSet, basename="group_mgmt")
router.register(r"user", UserViewSet, basename="user_mgmt")
router.register(r"role", RoleViewSet, basename="role_mgmt")
urlpatterns = router.urls
