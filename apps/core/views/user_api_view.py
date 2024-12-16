from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.decorators.api_perminssion import HasRole
from apps.core.models import UserAPISecret
from apps.core.serializers.user_auth_serializer import UserAPISecretSerializer


class UserAPISecretViewSet(viewsets.ModelViewSet):
    queryset = UserAPISecret.objects.all()
    serializer_class = UserAPISecretSerializer
    ordering = ("-id",)

    def list(self, request, *args, **kwargs):
        query = self.get_queryset().filter(username=request.user.username)
        queryset = self.filter_queryset(query)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["POST"])
    def generate_api_secret(self, request):
        api_secret = UserAPISecret.generate_api_secret()
        return JsonResponse({"result": True, "data": {"api_secret": api_secret}})

    @HasRole()
    def create(self, request, *args, **kwargs):
        username = request.user.username
        if UserAPISecret.objects.filter(username=username).exists():
            return JsonResponse({"result": False, "message": _("This user already has an API Secret")})
        kwargs = {
            "username": username,
            "api_secret": UserAPISecret.generate_api_secret(),
            "team": request.data.get("team"),
        }
        serializer = self.get_serializer(data=kwargs)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return JsonResponse({"result": False, "message": "API密钥不支持修改"})

    @HasRole()
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
