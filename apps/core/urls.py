from django.contrib import admin
from django.urls import re_path
from rest_framework import routers

from apps.core.views import index_view
from apps.core.views.user_view import UserView

admin.site.site_title = "OpsPilot"
admin.site.site_header = admin.site.site_title
public_router = routers.DefaultRouter()
public_router.register(r"api/public/user_view", UserView, basename="user_view")
urlpatterns = [
    re_path(r"^login_info/$", index_view.login_info),
]

urlpatterns += public_router.urls
