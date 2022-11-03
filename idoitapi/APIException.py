from typing import Any


class APIException(Exception):
    """
    Exceptions thrown by i-doit API modules
    """
    pass


class JSONRPC(APIException):
    code: int = None
    # code_min: int = None
    # code_max: int = None
    message: str = ""
    meaning: str = ""

    def __init__(self, data: Any = None, raw_code: int = None, message: str = None) -> None:
        APIException.__init__(self)
        self.data = data
        self.raw_code = raw_code
        self.message = message

    def __str__(self) -> str:
        return "{message} ({code}) - {meaning}".format(
            message=self.message,
            code=self.code or self.raw_code,
            meaning=self.meaning
        )

    def __repr__(self) -> str:
        return "{message} ({code}) - {meaning} {data}".format(
            message=self.message,
            code=self.code or self.raw_code,
            meaning=self.meaning,
            data=repr(self.data)
        )


class InvalidParams(JSONRPC):
    code = -32602
    message = 'Invalid params'
    meaning = 'Invalid method parameter(s).'


class InternalError(JSONRPC):
    code = -32603
    message = 'Internal error'
    meaning = 'Internal JSON-RPC error.'


class MethodNotFound(JSONRPC):
    code = -32601
    message = 'Method not found'
    meaning = 'The method does not exist / is not available.'


class UnknownError(JSONRPC):
    code = None
    message = 'Unknown error'
    meaning = 'An unknown error occurred'
