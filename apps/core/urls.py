from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers

from apps.core.views import index_view

admin.site.site_title = "SystemMgmt"
admin.site.site_header = admin.site.site_title
public_router = routers.DefaultRouter()
urlpatterns = [
    re_path(r"api/login_info/", index_view.login_info),
    re_path(r"api/get_client/", index_view.get_client),
    re_path(r"api/get_my_client/", index_view.get_my_client),
    re_path(r"api/get_client_detail/", index_view.get_client_detail),
    re_path(r"api/get_user_menus/", index_view.get_user_menus),
    path("select2/", include("django_select2.urls")),
]

urlpatterns += public_router.urls
