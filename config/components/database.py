# 数据库配置
import os
from pathlib import Path

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

db_engine = os.getenv('DB_ENGINE', 'postgresql').lower()

if db_engine == 'postgresql':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("DB_USER"),
            "PASSWORD": os.getenv("DB_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
        }
    }
if db_engine == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(Path(__file__).resolve().parent.parent, 'rewind.sqlite3'),
        }
    }
