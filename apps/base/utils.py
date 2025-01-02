from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature

from apps.core.logger import logger


class WeChatUtils(object):
    @staticmethod
    def signature_check(req_get_params):
        signature = req_get_params.get("signature", "")
        timestamp = req_get_params.get("timestamp", "")
        nonce = req_get_params.get("nonce", "")
        token = "022820"
        try:
            check_signature(token, signature, timestamp, nonce)
            return True
        except InvalidSignatureException as e:
            logger.exception("wechat signature error: %s" % e)
            return False
