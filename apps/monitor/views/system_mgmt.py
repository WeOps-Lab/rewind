from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

from apps.core.utils.web_utils import WebUtils
from apps.monitor.utils.system_mgmt_api import SystemMgmtUtils


class SystemMgmtView(ViewSet):
    @swagger_auto_schema(
        operation_description="查询所有用户",
        tags=['SystemMgmt']
    )
    @action(methods=['get'], detail=False, url_path='user_all')
    def get_user_all(self, request):
        data = SystemMgmtUtils.get_user_all()
        return WebUtils.response_success(data)

    @swagger_auto_schema(
        operation_description="查询通知渠道",
        tags=['SystemMgmt']
    )
    @action(methods=['get'], detail=False, url_path='search_channel_list')
    def search_channel_list(self, request):
        data = SystemMgmtUtils.search_channel_list()
        return WebUtils.response_success(data)
