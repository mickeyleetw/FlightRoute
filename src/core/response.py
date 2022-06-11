import enum

from pydantic import BaseModel
from starlette import status


@enum.unique
class ErrorCode(enum.IntEnum):
    GENERAL_1001_UNEXPECTED_ERROR = 1001
    GENERAL_1002_REQUEST_VALIDATION_FAILED = 1002
    GENERAL_1003_REQUEST_VALIDATION_FAILED = 1003

    RESOURCE_2001_NOT_FOUND = 2001


class ErrorMessage(BaseModel):
    code: int
    message: str


default_responses: dict = {
    status.HTTP_422_UNPROCESSABLE_ENTITY:
        {
            'model': ErrorMessage,
            'description': 'Validation error',
            'content':
                {
                    'application/json':
                        {
                            'example':
                                {
                                    'code': ErrorCode.GENERAL_1002_REQUEST_VALIDATION_FAILED,
                                    'message': 'validation error'
                                }
                        }
                },
        },
    status.HTTP_500_INTERNAL_SERVER_ERROR:
        {
            'model': ErrorMessage,
            'description': 'Internal error',
            'content':
                {
                    'application/json':
                        {
                            'example': {
                                'code': ErrorCode.GENERAL_1001_UNEXPECTED_ERROR,
                                'message': 'internal error'
                            }
                        }
                },
        }
}


def response_404(subject: str) -> dict:
    return {
        status.HTTP_404_NOT_FOUND:
            {
                'model': ErrorMessage,
                'description': f'{subject} not found',
                'content':
                    {
                        'application/json':
                            {
                                'example': {
                                    'code': ErrorCode.RESOURCE_2001_NOT_FOUND,
                                    'message': 'resource not found'
                                }
                            }
                    },
            }
    }


def response_428(message: str) -> dict:
    return {
        status.HTTP_428_PRECONDITION_REQUIRED:
            {
                'model': ErrorMessage,
                'description': 'Forbidden',
                'content':
                    {
                        'application/json':
                            {
                                'example':
                                    {
                                        'code': ErrorCode.GENERAL_1003_REQUEST_VALIDATION_FAILED,
                                        'message': message
                                    }
                            }
                    }
            }
    }
