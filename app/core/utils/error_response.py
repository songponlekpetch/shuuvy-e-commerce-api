import traceback
from django.http import JsonResponse
from django.conf import settings

class ErrorJsonResponse(JsonResponse):
    def __init__(self, data, status):
        self.data = data
        self.status = status

        if settings.DEBUG:
            self.data["traceback"] = traceback.format_exc().splitlines()

        super().__init__(self.data, content_type="application/json", status=self.status )
