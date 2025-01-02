from rest_framework import serializers

from apps.base.models import UserAPISecret


class UserAPISecretSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAPISecret
        fields = "__all__"
