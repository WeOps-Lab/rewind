# settings.py
import os
from datetime import timedelta
from typing import List, Tuple
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "")
APP_CODE = os.getenv("APP_CODE", "munchkin")

# 使用时区
USE_TZ = True

# 时区设置
# TIME_ZONE = "Asia/Shanghai"
TIME_ZONE = "UTC"

# 语言设置
LANGUAGE_CODE = "zh-Hans"
# 国际化设置
USE_I18N = True
# 本地化设置
USE_L10N = True

# 定义支持的语言
LANGUAGES = (
    ("en", "English"),
    ("zh-Hans", "简体中文"),
)
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
SESSION_COOKIE_NAME = f"{APP_CODE}_sessionid"
LOGIN_CACHE_EXPIRED = 60 * 60

# email配置

# 指定邮件发送的后端，用于处理邮件发送逻辑。
# 默认使用SMTP后端，支持通过SMTP服务器发送邮件。
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')

# SMTP服务器的主机地址，例如 Gmail 的是 'smtp.gmail.com'。
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')

# SMTP服务器端口号。
# 通常：
# - 587 用于 TLS 加密连接。
# - 465 用于 SSL 加密连接。
# - 25 用于非加密连接（不推荐）。
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))

# 是否启用 TLS（传输层安全协议），用于加密邮件传输。
# 如果SMTP服务支持TLS，通常设置为True（典型端口号为587）。
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'

# 是否启用 SSL（安全套接字层协议），用于加密邮件传输。
# 如果SMTP服务只支持SSL，通常设置为True（典型端口号为465）。
# 注意：EMAIL_USE_SSL 和 EMAIL_USE_TLS 不能同时为 True。
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False') == 'True'

# 邮件服务器的登录用户名，通常是完整的邮箱地址。
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'your_email@example.com')

# 邮件服务器的登录密码或授权码（某些邮箱需要单独设置授权码）。
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'your_password')

# 发件人的默认邮箱地址，显示在收件人邮箱的“发件人”字段。
# 格式可以是简单的邮箱地址或带有昵称的形式，如 'Your App <your_email@example.com>'。
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'Your App <your_email@example.com>')

# 设置邮件发送超时时间（以秒为单位）。
# 如果邮件服务器在指定时间内没有响应，Django 会抛出超时异常。
EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', 5))

# 邮件主题的前缀，会附加到每封邮件的主题开头。
# 便于在用户的收件箱中快速识别邮件来源。
EMAIL_SUBJECT_PREFIX = os.getenv('EMAIL_SUBJECT_PREFIX', '[WeOps]')

# CSRF配置
CSRF_COOKIE_NAME = f"{APP_CODE}_csrftoken"

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 指定翻译文件的目录
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = (
    "apps.base",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "django_minio_backend",
    "django_filters",
    "mptt",
    "django_comment_migrate",
    "import_export",
    "django_select2",
    "apps.core",
)
IS_USE_CELERY = True

ASGI_APPLICATION = "asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

MIDDLEWARE = (
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    # 跨域检测中间件， 默认关闭
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # django国际化中间件
    "django.middleware.locale.LocaleMiddleware",
    "apps.core.middlewares.app_exception_middleware.AppExceptionMiddleware",
    "apps.core.middlewares.drf_middleware.DisableCSRFMiddleware",
    "apps.core.middlewares.api_middleware.APISecretMiddleware",
    "apps.core.middlewares.keycloak_auth_middleware.KeyCloakAuthMiddleware",
)
AUTHENTICATION_BACKENDS = (
    "apps.core.backends.KeycloakAuthBackend",  # this is default
    "apps.core.backends.APISecretAuthBackend",
    # "django.contrib.auth.backends.ModelBackend",
)
ROOT_URLCONF = "urls"

AUTH_USER_MODEL = "base.User"

DEBUG = os.getenv("DEBUG", "0") == "1"

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles/")

if DEBUG:
    INSTALLED_APPS += (
        "corsheaders",
        "drf_yasg",
        "debug_toolbar",
    )  # noqa
    # 该跨域中间件需要放在前面
    MIDDLEWARE = (
                     "corsheaders.middleware.CorsMiddleware",
                     "debug_toolbar.middleware.DebugToolbarMiddleware",
                 ) + MIDDLEWARE  # noqa
    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOW_HEADERS = [
        "accept",
        "authorization",
        "content-type",
        "user-agent",
        "x-csrftoken",
        "x-requested-with",
        "api-authorization",
        "debug",
    ]
# 缓存配置
REDIS_CACHE_URL = os.environ.get("REDIS_CACHE_URL", "")

CACHES = {
    "db": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "django_cache",
    },
    "dummy": {"BACKEND": "django.core.cache.backends.dummy.DummyCache"},
    "locmem": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    "redis": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": REDIS_CACHE_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    },
}
if REDIS_CACHE_URL:
    CACHES["default"] = CACHES["redis"]
else:
    CACHES["default"] = CACHES["locmem"]

# 模板页面配置
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": (os.path.join(BASE_DIR, "templates"),),
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "config.context_processors.web_env.custom_settings",
            ],
        },
    }
]

# 数据库配置
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),  # 替换为你的数据库名称
        "USER": os.getenv("DB_USER"),  # 替换为你的数据库用户
        "PASSWORD": os.getenv("DB_PASSWORD"),  # 替换为你的数据库密码
        "HOST": os.getenv("DB_HOST"),  # 通常是 'localhost' 或者是数据库服务器的 IP 地址
        "PORT": os.getenv("DB_PORT"),  # 通常是 '5432'，如果你使用的是默认端口的话
    }
}

# celery
CELERY_IMPORTS = ()
CELERY_TIMEZONE = TIME_ZONE  # celery 时区问题
CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL", "amqp://admin:password@rabbitmq.lite/"
)

if IS_USE_CELERY:
    INSTALLED_APPS = locals().get("INSTALLED_APPS", [])
    INSTALLED_APPS += (
        "django_celery_beat",
        "django_celery_results",
    )
    CELERY_ENABLE_UTC = False
    CELERY_WORKER_CONCURRENCY = 2  # 并发数
    CELERY_MAX_TASKS_PER_CHILD = 5  # worker最多执行5个任务便自我销毁释放内存
    CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
    CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
    CELERY_ACCEPT_CONTENT = ["application/json"]
    CELERY_TASK_SERIALIZER = "json"
    CELERY_RESULT_SERIALIZER = "json"
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")
    DJANGO_CELERY_BEAT_TZ_AWARE = False
# 获取 apps 目录下的所有子目录名称
APPS_DIR = os.path.join(BASE_DIR, "apps")
if os.path.exists(APPS_DIR):
    app_folders = [
        name
        for name in os.listdir(APPS_DIR)
        if os.path.isdir(os.path.join(APPS_DIR, name)) and name not in  ["__pycache__", "base", "core"]
    ]
else:
    app_folders = []
INSTALLED_APPS += tuple(f"apps.{app}" for app in app_folders)
# DRF 配置

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_PAGINATION_CLASS": "config.drf.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": 10,
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    # "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATETIME_FORMAT": "%Y-%m-%dT%H:%M:%S%z",
    "NON_FIELD_ERRORS_KEY": "params_error",
    "DEFAULT_RENDERER_CLASSES": ("config.drf.renderers.CustomRenderer",),
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
}

AUTH_TOKEN_HEADER_NAME = "HTTP_AUTHORIZATION"
API_TOKEN_HEADER_NAME = "HTTP_API_AUTHORIZATION"
# keycloak配置
KEYCLOAK_URL_API = os.getenv("KEYCLOAK_URL_API")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USERNAME")
KEYCLOAK_ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")

# 日志配置
if DEBUG:
    log_dir = os.path.join(os.path.dirname(BASE_DIR), "logs", APP_CODE)
else:
    LOG_DIR = os.getenv("LOG_DIR", "/tmp/logs/")
    log_dir = os.path.join(os.path.join(LOG_DIR, APP_CODE))

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {"format": "%(levelname)s %(message)s \n"},
        "verbose": {
            "format": "%(levelname)s [%(asctime)s] %(pathname)s "
                      "%(lineno)d %(funcName)s %(process)d %(thread)d "
                      "\n \t %(message)s \n",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
        "root": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(log_dir, "%s.log" % APP_CODE),
        },
        "db": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "verbose",
            "filename": os.path.join(log_dir, "db.log"),
        },
    },
    "loggers": {
        "django": {"handlers": ["null"], "level": "INFO", "propagate": True},
        "django.server": {"handlers": ["console"], "level": "INFO", "propagate": True},
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
        "django.db.backends": {"handlers": ["db"], "level": "INFO", "propagate": True},
        "app": {"handlers": ["root", "console"], "level": "DEBUG", "propagate": True},
        "celery": {"handlers": ["root"], "level": "INFO", "propagate": True},
    },
}
# MINIO 配置
# MINIO_EXTERNAL_ENDPOINT = os.getenv("MINIO_EXTERNAL_ENDPOINT")
# MINIO_EXTERNAL_ENDPOINT_USE_HTTPS = os.getenv("MINIO_EXTERNAL_ENDPOINT_USE_HTTPS", "0") == "1"
MINIO_BUCKET_CHECK_ON_SAVE = True
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_USE_HTTPS = os.getenv("MINIO_USE_HTTPS", "0") == "1"
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_URL_EXPIRY_HOURS = timedelta(days=7)
MINIO_CONSISTENCY_CHECK_ON_START = False

MINIO_PRIVATE_BUCKETS = ["rewind-private"]
MINIO_PUBLIC_BUCKETS = ["rewind-public"]
MINIO_POLICY_HOOKS: List[Tuple[str, dict]] = []

from apps.config import *  # noqa

# 本地设置
try:
    from local_settings import *  # noqa
except ImportError:
    pass
