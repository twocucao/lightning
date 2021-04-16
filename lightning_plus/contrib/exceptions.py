import logging
import traceback
from typing import List, Any

from django.http import JsonResponse


class ApiException(Exception):
    code = 2400
    message = ""
    errors: List[Any]

    def __init__(self, message):
        self.message = message


class NotFound(ApiException):
    code = 2404


class PermissionDenied(ApiException):
    code = 2403


class AuthFailed(ApiException):
    code = 2401


logger = logging.getLogger(__name__)


def format_exc(exc) -> str:
    stack = traceback.extract_stack()[:-3] + traceback.extract_tb(
        exc.__traceback__
    )  # add limit=??
    pretty = traceback.format_list(stack)
    return "".join(pretty) + "\n  {} {}".format(exc.__class__, exc)


def exception_handler(exc):
    if isinstance(exc, ApiException):
        data = {"message": exc.message}
        return JsonResponse(data)

    data = {"message": "服务器繁忙"}
    logger.exception("服务器繁忙", exc_info=(exc.__class__, exc, exc.__traceback__))
    # if is_not_prod():
    #     data["traceback"] = format_exc(exc)
    return JsonResponse(data)