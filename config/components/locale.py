# 使用时区
import os

from config.components.base import BASE_DIR

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


# 指定翻译文件的目录
LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
