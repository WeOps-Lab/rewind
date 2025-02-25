import datetime
import json
import time

import pika
from django.conf import settings
from django.core.management import BaseCommand
from django.db import close_old_connections

from apps.bot_mgmt.models import Bot, BotConversationHistory
from apps.bot_mgmt.models.channel_user import ChannelUser
from apps.bot_mgmt.utils import get_user_info
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
            user, _ = get_user_info(bot_id, input_channel, sender_id)
            bot = Bot.objects.get(id=bot_id)
            msg = message.get("metadata", {}).get("other_data", {}).get("citing_knowledge", [])
            msg_str = json.dumps(msg).replace("\u0000", " ")
            BotConversationHistory.objects.get_or_create(
                bot_id=bot_id,
                channel_user_id=user.id,
                created_at=created_at,
                created_by=bot.created_by,
                conversation_role=message["event"],
                conversation=message["text"] or "",
                citing_knowledge=json.loads(msg_str),
            )
    except Exception as e:
        logger.exception(f"对话历史保存失败: {e}")
    else:
        logger.info("消息处理完成")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


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
                channel.queue_declare(queue="pilot", durable=True)
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
