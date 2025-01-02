import base64

import xmltodict
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.http import HttpResponse
from wechatpy import parse_message
from wechatpy.replies import TextReply
from wechatpy.utils import to_text

from apps.base.utils import WeChatUtils
from apps.core.utils.exempt import api_exempt


@api_exempt
def test(request):
    signature_check_result = WeChatUtils.signature_check(request.GET)
    if request.method == "GET":
        if signature_check_result:
            return HttpResponse(request.GET.get("echostr"))
        else:
            return HttpResponse("Access failed!")
    if request.method == "POST":
        if not signature_check_result:
            return HttpResponse("Access failed!")
        xml_msg = xmltodict.parse(to_text(request.body))["xml"]
        decode_msg = decrypt(xml_msg["Encrypt"])
        msg = parse_message(decode_msg)
        reply = TextReply(message=msg)
        if msg.type == "text":
            reply.content = "我什么都不想说"
        else:
            reply.content = "感谢关注统一告警中心！"
        xml = reply.render()
        return HttpResponse(xml)


def decrypt(msg_encrypt):
    encoding_aes_key = "HvFkbaedy74IHLno7Q8BHGV94m593uStMVXAKasjUCu"
    aes_key = base64.b64decode(encoding_aes_key + "=")
    try:
        cipher = AES.new(aes_key, AES.MODE_CBC, aes_key[:16])
        ciphertext_decoded = base64.b64decode(msg_encrypt)
        plaintext_padded = cipher.decrypt(ciphertext_decoded)
        plaintext = unpad(plaintext_padded, AES.block_size)
        xml_len = int.from_bytes(plaintext[16:20], byteorder="big")
        xml_content = plaintext[20 : 20 + xml_len].decode("utf-8")
        return xml_content
    except Exception as e:
        print(e)
        return None
