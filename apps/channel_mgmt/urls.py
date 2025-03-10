from rest_framework import routers

from apps.channel_mgmt.viewset import ChannelViewSet

router = routers.DefaultRouter()
router.register(r"channel", ChannelViewSet)
urlpatterns = router.urls
