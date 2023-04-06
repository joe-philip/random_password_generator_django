from logging import error

from django.conf import settings
from rest_framework import exceptions
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from root.utils.utils import fail


def custom_exception_handler(exc, context):
    if isinstance(exc, APIException):
        exception = exc
    else:
        if settings.DEBUG:
            print(str(exc))
        error(msg=str(exc)+f'\n{type(exc)}')
        exception = APIException()
        exception.status_code = 500
        exception.detail = 'Server error please contact your system Administrator'
    if isinstance(exception, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait
        if isinstance(exception.detail, (list, dict)):
            data = fail(exception.detail)
        else:
            data = fail(str(exception.detail))
        return Response(data, status=exception.status_code, headers=headers)
    return None
