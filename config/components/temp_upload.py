import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# 设置临时文件存储目录
FILE_UPLOAD_TEMP_DIR = os.path.join(BASE_DIR, 'temp_uploads')
os.makedirs(FILE_UPLOAD_TEMP_DIR, exist_ok=True)

# 设置直接读入内存的最大上传文件大小（默认2.5MB）
# FILE_UPLOAD_MAX_MEMORY_SIZE = 2.5 * 1024 * 1024
