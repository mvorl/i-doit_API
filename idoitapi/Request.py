from typing import List, Dict

from idoitapi.API import API
from idoitapi.APIException import JSONRPC


class Request(object):
    """
    Base class for JSON RPC API requests
    """

    def __init__(self, api: API = None, api_params: Dict = None) -> None:
        """
        :param api: (optional) a :py:mod:`~idoitapi.API` object
        :param dict api_params: (optional) parameters to pass to the API
        """
        if api is None:
            if api_params is None:
                api_params = {}
            api = API(**api_params)
        self._api = api

    @staticmethod
    def require_success_for(result: Dict) -> int:
        """
        Check for success and return identifier

        :param dict result: Response from API request
        :return: Identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if 'id' not in result or not isinstance(result['id'], int) or \
                'success' not in result or not result['success']:
            message = 'Bad result'
            if 'message' in result:
                message += ': ' + result['message']
            raise JSONRPC(message=message)

        return result['id']

    @staticmethod
    def require_success_without_identifier(result: Dict) -> None:
        """
        Check for success but ignore identifier

        :param dict result: Result
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if 'success' not in result or not result['success']:
            message = 'Bad result'
            if 'message' in result:
                message += ': ' + result['message']
            raise JSONRPC(message=message)

    @staticmethod
    def require_success_for_all(results: List[Dict]) -> None:
        """
        Check whether each request in a batch was successful

        :param list[dict] results: Results
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        for result in results:
            Request.require_success_without_identifier(result)
