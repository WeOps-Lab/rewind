from rest_framework import routers

from apps.nats_demo.views import DemoViewSet

router = routers.DefaultRouter()

router.register(r'api/nats_demo', DemoViewSet, basename='demo')

urlpatterns = router.urls
