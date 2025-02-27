from rest_framework import routers

from apps.channel_mgmt.viewset import ChannelTemplateViewSet, ChannelViewSet

router = routers.DefaultRouter()
router.register(r"channel", ChannelViewSet)
router.register(r"channel_template", ChannelTemplateViewSet)
urlpatterns = router.urls
