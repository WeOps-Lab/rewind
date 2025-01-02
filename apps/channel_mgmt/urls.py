from rest_framework import routers

from apps.channel_mgmt.views.channel_view_set import ChannelViewSet

router = routers.DefaultRouter()
router.register(r"channel", ChannelViewSet)
urlpatterns = router.urls

urlpatterns += []
