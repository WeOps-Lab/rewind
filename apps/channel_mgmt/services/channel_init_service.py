from apps.core.logger import logger


class ChannelInitService:
    def __init__(self, owner):
        self.owner = owner.username

    @staticmethod
    def init():
        logger.info("初始化监控告警模板")
