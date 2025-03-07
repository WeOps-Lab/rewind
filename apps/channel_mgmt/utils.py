import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from wechatpy import WeChatClientException
from wechatpy.enterprise import WeChatClient

from apps.channel_mgmt.models import Channel


def send_wechat(channel_obj: Channel, content, receivers):
    """发送企业微信消息"""
    channel_config = channel_obj.config
    channel_obj.encrypt_field("secret", channel_config)
    channel_obj.encrypt_field("token", channel_config)
    channel_obj.encrypt_field("aes_key", channel_config)
    try:
        # 创建企业微信客户端
        client = WeChatClient(corp_id=channel_config["corp_id"], secret=channel_config["secret"])
        # 发送文本消息
        client.message.send_text(agent_id=channel_config["agent_id"], user_ids=receivers, content=content)
        return {"result": True, "message": "Successfully sent WeChat message"}
    except WeChatClientException as e:
        return {"result": False, "message": f"WeChat API error: {e.errmsg}"}
    except Exception as e:
        return {"result": False, "message": f"Error sending WeChat message: {str(e)}"}


def send_email(channel_obj: Channel, title, content, receivers):
    """发送邮件"""
    channel_config = channel_obj.config
    channel_obj.encrypt_field("smtp_pwd", channel_config)
    try:
        msg = MIMEMultipart()
        msg["From"] = channel_config["mail_sender"]
        msg["To"] = receivers
        msg["Subject"] = title

        msg.attach(MIMEText(content, "plain", "utf-8"))

        # 根据配置决定使用 SSL 还是普通连接
        if channel_config.get("smtp_usessl", False):
            server = smtplib.SMTP_SSL(channel_config["smtp_server"], channel_config["port"])
        else:
            server = smtplib.SMTP(channel_config["smtp_server"], channel_config["port"])

        # 如果配置使用 TLS，则启用 TLS
        if channel_config.get("smtp_usetls", False):
            server.starttls()

        server.login(channel_config["smtp_user"], channel_config["smtp_pwd"])
        server.send_message(msg)
        server.quit()

        return {"result": True, "message": "Successfully sent email"}
    except Exception as e:
        return {"result": False, "message": f"Error sending email: {str(e)}"}
