import json
from functools import wraps

def json_dumps_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # 调用被装饰的函数
        result = func(*args, **kwargs)
        return json.dumps(result)

    return wrapper
