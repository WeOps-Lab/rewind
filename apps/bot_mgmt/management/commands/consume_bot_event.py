import datetime
import json
import time

import pika
from django.conf import settings
from django.core.management import BaseCommand
from django.db import close_old_connections
from wechatpy import WeChatClient as WeChatAccountClient
from wechatpy.enterprise import WeChatClient

from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.bot_mgmt.models.bot import BotChannel
from apps.bot_mgmt.models.channel_user import ChannelUser
from apps.bot_mgmt.services.ding_talk_client import DingTalkClient
from apps.channel_mgmt.models import ChannelChoices
from apps.core.logger import logger

channel_map = {}


def on_message(channel, method_frame, header_frame, body):
    try:
        message = json.loads(body.decode())
        logger.info(f"开始处理消息: {message}")
        if "text" in message:
            close_old_connections()
            sender_id = message["sender_id"]
            bot_id = int(message.get("bot_id", 7))
            created_at = datetime.datetime.fromtimestamp(message["timestamp"], tz=datetime.timezone.utc)
            if "input_channel" in message:
                input_channel = message["input_channel"]
                channel_map[sender_id] = input_channel
            else:
                input_channel = channel_map.get(sender_id)
                if not input_channel:
                    channel_user = ChannelUser.objects.get(user_id=sender_id)
                    input_channel = (
                        channel_user.channel_type if channel_user.channel_type != ChannelChoices.WEB else "socketio"
                    )
            user = get_user_info(bot_id, input_channel, sender_id)
            bot = Bot.objects.get(id=bot_id)
            BotConversationHistory.objects.get_or_create(
                bot_id=bot_id,
                channel_user_id=user.id,
                created_at=created_at,
                created_by=bot.created_by,
                conversation_role=message["event"],
                conversation=message["text"] or "",
                citing_knowledge=message.get("metadata", {}).get("other_data", {}).get("citing_knowledge", []),
            )
    except Exception as e:
        logger.exception(f"对话历史保存失败: {e}")
    else:
        logger.info("消息处理完成")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def get_user_info(bot_id, input_channel, sender_id):
    channel_type_map = {
        "socketio": ChannelChoices.WEB,
        "enterprise_wechat": ChannelChoices.ENTERPRISE_WECHAT,
        "dingtalk": ChannelChoices.DING_TALK,
        "wechat_official_account": ChannelChoices.WECHAT_OFFICIAL_ACCOUNT,
    }
    if input_channel == "enterprise_wechat":
        channel_obj = BotChannel.objects.get(bot_id=bot_id, channel_type=ChannelChoices.ENTERPRISE_WECHAT)
        conf = channel_obj.decrypted_channel_config
        wechat_client = WeChatClient(
            conf["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]["corp_id"],
            conf["channels.enterprise_wechat_channel.EnterpriseWechatChannel"]["secret"],
        )
        try:
            name = wechat_client.user.get(sender_id)["name"]
        except Exception as e:
            logger.error(f"获取企业微信用户信息失败: {e}")
            name = sender_id
    elif input_channel == "dingtalk":
        channel_obj = BotChannel.objects.get(bot_id=bot_id, channel_type=ChannelChoices.DING_TALK)
        conf = channel_obj.decrypted_channel_config
        client = DingTalkClient(
            conf["channels.dingtalk_channel.DingTalkChannel"]["client_id"],
            conf["channels.dingtalk_channel.DingTalkChannel"]["client_secret"],
        )
        try:
            name = client.get_user_info(sender_id)["name"]
        except Exception as e:
            logger.error(f"获取钉钉用户信息失败: {e}")
            name = sender_id
    elif input_channel == "wechat_official_account":
        channel_obj = BotChannel.objects.get(bot_id=bot_id, channel_type=ChannelChoices.WECHAT_OFFICIAL_ACCOUNT)
        conf = channel_obj.decrypted_channel_config
        client = WeChatAccountClient(
            conf["channels.wechat_official_account_channel.WechatOfficialAccountChannel"]["appid"],
            conf["channels.wechat_official_account_channel.WechatOfficialAccountChannel"]["secret"],
        )
        try:
            user = client.user.get(sender_id)
            name = user["nickname"] or user["remark"] or sender_id
        except Exception as e:
            logger.error(f"获取微信用户信息失败: {e}")
            name = sender_id
    else:
        name = sender_id

    if name == sender_id:
        fun = "get_or_create"
    else:
        fun = "update_or_create"

    user, _ = getattr(ChannelUser.objects, fun)(
        user_id=sender_id, channel_type=channel_type_map[input_channel], defaults={"name": name}
    )

    return user


class Command(BaseCommand):
    help = "获取对话历史"

    def handle(self, *args, **options):
        logger.info(f"初始化消息队列连接:[{settings.CONVERSATION_MQ_HOST}:{settings.CONVERSATION_MQ_PORT}]")
        connection = None
        while True:
            try:
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=settings.CONVERSATION_MQ_HOST,
                        port=settings.CONVERSATION_MQ_PORT,
                        credentials=pika.PlainCredentials(
                            settings.CONVERSATION_MQ_USER, settings.CONVERSATION_MQ_PASSWORD
                        ),
                    )
                )
                channel = connection.channel()
                channel.basic_consume("pilot", on_message)
                try:
                    channel.start_consuming()
                except KeyboardInterrupt:
                    channel.stop_consuming()
                connection.close()
            except Exception as e:
                logger.exception(f"消息队列连接失败:{e}")
            finally:
                if connection is not None and getattr(connection, "is_open", False):
                    connection.close()
                time.sleep(60)
