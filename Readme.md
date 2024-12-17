# 开发环境

1. 安装依赖

```
make setup
make install
```

2. 在根目录下创建`local_settings.py`文件

```
import os

from config.default import BASE_DIR

SECRET_KEY = "django-in-secure-secret-key"
CELERY_BROKER_URL = "sqla+sqlite:///celerydb.sqlite3"
CELERY_RESULT_BACKEND = "db+sqlite:///celerydb.sqlite3"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
```

3. 初始化数据库

```
make migrate
```
