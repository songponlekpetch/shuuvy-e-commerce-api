import logging
import traceback

from core.utils.exceptions import BaseException
from core.utils.error_response import ErrorJsonResponse

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(f"path: {request.path}")
        logger.error(f"request: {request.POST}")
        if isinstance(exception, BaseException):
            response = ErrorJsonResponse(
                dict(
                    message=exception.message,
                    error_code=exception.code,),
                status=exception.http_code,
            )

            logger.error(f"message: {exception.message}")
            logger.error(f"error_code: {exception.code}")
            logger.error(f"http_code: {exception.http_code}")
            logger.error(traceback.format_exc().splitlines())

            return response
        else:
            response = ErrorJsonResponse(
                dict(
                    message=str(exception),
                    error_code=500),
                status=500,
            )

            logger.error(f"message: {exception}")
            logger.error(f"error_code: 500")
            logger.error(f"http_code: 500")
            logger.error(traceback.format_exc().splitlines())

            return response
