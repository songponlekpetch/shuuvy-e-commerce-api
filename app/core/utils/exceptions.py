class BaseException(Exception):

    def __init__(self, message, code, http_code):
        self.message = message
        self.code = code
        self.http_code = http_code
        super().__init__(message)
