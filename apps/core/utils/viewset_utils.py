from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response


class AuthViewSet(viewsets.ModelViewSet):
    def query_by_groups(self, request, queryset):
        if not request.user.is_superuser:
            teams = [i["id"] for i in request.user.group_list]
            query = Q()
            for team_member in teams:
                query |= Q(team__contains=team_member)
            queryset = queryset.filter(query)
        return self._list(queryset.order_by("-id"))

    def _list(self, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """创建时补充基础Model中的字段"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        if hasattr(serializer.Meta.model, "created_by"):
            serializer.save(created_by=username, updated_by=username)

    def perform_update(self, serializer):
        """更新时补充基础Model中的字段"""
        user = serializer.context.get("request").user
        username = getattr(user, "username", "guest")
        if hasattr(serializer.Meta.model, "updated_by"):
            serializer.save(updated_by=username)
