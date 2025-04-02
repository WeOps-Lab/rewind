
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from apps.node_mgmt.utils.s3 import upload_file_to_s3, get_s3_download_url
from config.components.temp_upload import FILE_UPLOAD_TEMP_DIR


class PackageService:
    @staticmethod
    def upload_file(file: ContentFile, package_obj):
        local_file_path = f"{FILE_UPLOAD_TEMP_DIR}/{package_obj.name}"

        # 接收文件到指定目录
        default_storage.save(local_file_path, ContentFile(file.read()))
        s3_file_path = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
        # 从指定目录上传文件到s3
        upload_file_to_s3(local_file_path, s3_file_path)

        # 删除临时文件
        if default_storage.exists(local_file_path):
            default_storage.delete(local_file_path)

    @staticmethod
    def get_download_url(package_obj):
        s3_file_path = f"{package_obj.os}/{package_obj.object}/{package_obj.version}/{package_obj.name}"
        return get_s3_download_url(s3_file_path)
