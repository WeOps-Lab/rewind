# -*- coding: utf-8 -*-
from dotenv import load_dotenv

load_dotenv()


def custom_settings(request):
    """
    :summary: 这里可以返回前端需要的公共变量
    :param request:
    :return:
    """
    # TODO 前端需要的环境变量
    context = {}
    return context
