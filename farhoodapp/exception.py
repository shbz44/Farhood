from django.utils import six
from rest_framework import status
from rest_framework.exceptions import APIException


class ValidationError(APIException):
    status_code = status.HTTP_404_NOT_FOUND

    def __init__(self, detail, status):
        """

        :param detail: details of error
        :param status: status code
        """
        if not isinstance(detail, dict) and not isinstance(detail, list):
            detail = [detail]
        self.detail = detail
        self.status_code = status

    def __str__(self):
        return six.text_type(self.detail)
