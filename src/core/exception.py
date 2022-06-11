from fastapi import status

from core.response import ErrorCode


class BaseException_(Exception):
    http_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    code = ErrorCode.GENERAL_1001_UNEXPECTED_ERROR
    message = 'Unexpected'

    def __init__(self, msg=None, **kwargs):
        if not msg:
            msg = self.message
        for k, v in kwargs.items():
            setattr(self, k, v)

        super().__init__(msg)


class ResourceNotFoundException(BaseException_):

    def __init__(self, subject: str):
        super().__init__(
            code=ErrorCode.RESOURCE_2001_NOT_FOUND,
            http_status=status.HTTP_404_NOT_FOUND,
            message=f'{subject} not found'
        )


class EmptyQueryParamsException(BaseException_):

    def __init__(self, msg: str):
        super().__init__(
            code=ErrorCode.GENERAL_1003_REQUEST_VALIDATION_FAILED,
            http_status=status.HTTP_428_PRECONDITION_REQUIRED,
            message=msg
        )
