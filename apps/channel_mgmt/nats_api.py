from django.utils.translation import gettext as _

import nats_client
from apps.channel_mgmt.models import Channel, ChannelChoices
from apps.channel_mgmt.utils import send_email, send_wechat


@nats_client.register
def search_channel_list(channel_type):
    channels = Channel.objects.all()
    if channel_type:
        channels = channels.filter(channel_type=channel_type)
    return {"result": True, "data": [i for i in channels.values("id", "name", "channel_type")]}


@nats_client.register
def send_msg_with_channel(channel_id, title, content, receivers):
    channel_obj = Channel.objects.filter(id=channel_id).first()
    if not channel_obj:
        return {"result": False, "message": _("Channel not found")}
    if channel_obj.channel_type == ChannelChoices.EMAIL:
        return send_email(channel_obj, title, content, receivers)
    return send_wechat(channel_obj, content, receivers)
