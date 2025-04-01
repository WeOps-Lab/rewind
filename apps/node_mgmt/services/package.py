
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.node_mgmt.utils.s3 import upload_file_to_s3
from config.components.temp_upload import FILE_UPLOAD_TEMP_DIR


class PackageService:
    @staticmethod
    def upload_file(file: ContentFile):
        temp_file_path = f"{FILE_UPLOAD_TEMP_DIR}/{file.name}"

        # 接收文件到指定目录
        default_storage.save(temp_file_path, ContentFile(file.read()))

        # 从指定目录上传文件到s3
        upload_file_to_s3(temp_file_path)

        # 删除临时文件
        if default_storage.exists(temp_file_path):
            default_storage.delete(temp_file_path)
