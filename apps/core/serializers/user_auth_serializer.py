from rest_framework import serializers

from apps.core.models import UserAPISecret


class UserAuthSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, help_text="用户名")
    password = serializers.CharField(required=True, help_text="密码")


class UserAPISecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAPISecret
        fields = "__all__"
