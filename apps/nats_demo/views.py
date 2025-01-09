from rest_framework.response import Response
from rest_framework.decorators import action
import nats_client
from adrf.viewsets import ViewSet


class DemoViewSet(ViewSet):

    async def list(self, request, *args, **kwargs):
        response_message = await nats_client.request('nats-demo', 'hello_message',
                                                     token="123", message="Hello from Django",
                                                     dict_example={"a": 1, "b": True})
        return Response(response_message)
