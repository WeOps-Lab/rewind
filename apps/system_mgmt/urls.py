from django.urls import path
from rest_framework import routers

from apps.system_mgmt import views
from apps.system_mgmt.viewset import GroupViewSet, RoleViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r"group", GroupViewSet, basename="group_mgmt")
router.register(r"user", UserViewSet, basename="user_mgmt")
router.register(r"role", RoleViewSet, basename="role_mgmt")
urlpatterns = router.urls

urlpatterns += [
    path(r"api/get_client/", views.get_client, name="get_client"),
    path(r"api/get_client_detail/", views.get_client_detail, name="get_client_detail"),
    path(r"api/verify_token/", views.verify_token, name="verify_token"),
    path(r"api/get_user_menus/", views.get_user_menus, name="get_user_menus"),
]
