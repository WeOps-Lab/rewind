from django_filters import filters
from django_filters.rest_framework import FilterSet
from rest_framework import viewsets

from apps.channel_mgmt.models import Channel
from apps.channel_mgmt.serializers import ChannelSerializer


class ObjFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")


class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    filterset_class = ObjFilter
