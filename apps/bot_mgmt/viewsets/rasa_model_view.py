from rest_framework.viewsets import ModelViewSet

from apps.bot_mgmt.models import RasaModel
from apps.bot_mgmt.serializers.rasa_model_serializer import RasaModelSerializer


class RasaModelViewSet(ModelViewSet):
    serializer_class = RasaModelSerializer
    queryset = RasaModel.objects.all()
