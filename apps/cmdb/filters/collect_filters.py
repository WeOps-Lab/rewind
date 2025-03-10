# -- coding: utf-8 --
# @File: collect_filters.py
# @Time: 2025/3/3 14:00
# @Author: windyzhao


from django_filters import CharFilter, FilterSet

from apps.cmdb.models.collect_model import CollectModels


class CollectModelFilter(FilterSet):
    # inst_id = NumberFilter(field_name="inst_id", lookup_expr="exact", label="实例ID")
    search = CharFilter(field_name="name", lookup_expr="icontains", label="模型ID")
    driver_type = CharFilter(field_name="driver_type", label="任务类型")
    exec_status = CharFilter(field_name="exec_status", label="任务类型")

    class Meta:
        model = CollectModels
        fields = ["search", "driver_type", "exec_status"]
