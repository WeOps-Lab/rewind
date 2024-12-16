from django.http import JsonResponse
from rest_framework import status


class WebUtils:
    @staticmethod
    def response_success(response_data={}):
        return JsonResponse({"data": response_data, "result": True, "message": ""}, status=status.HTTP_200_OK)

    @staticmethod
    def response_error(response_data={}, error_message="", status_code=status.HTTP_400_BAD_REQUEST):
        return JsonResponse({"data": response_data, "result": False, "message": error_message}, status=status_code)

    @staticmethod
    def response_401(message):
        return JsonResponse({"result": False, "message": message}, status=status.HTTP_401_UNAUTHORIZED)

    @staticmethod
    def response_403(message):
        return JsonResponse({"result": False, "message": message}, status=status.HTTP_403_FORBIDDEN)
