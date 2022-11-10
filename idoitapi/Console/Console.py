from typing import List, Dict, Any

from idoitapi.APIException import JSONRPC
from idoitapi.Request import Request


class Console(Request):
    """
    Requests for API namespace 'console'
    """

    def execute(self, method: str, options: Dict = None, arguments: List[str] = None) -> List[str]:
        """
        Execute command

        :param str method: Method name
        :param dict options: List of options as key-value store
        :param list[str] arguments: List of arguments as strings
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Any] = {}

        if isinstance(options, dict) and len(options) > 0:
            params['options'] = options

        if isinstance(arguments, list) and len(arguments) > 0:
            params['arguments'] = arguments

        result = self._api.request(method, params)

        if 'success' not in result:
            raise JSONRPC(message='Missing success status')

        if not result['success']:
            raise JSONRPC(message='Command failed')

        if 'output' not in result:
            raise JSONRPC(message='Missing output')

        if not isinstance(result['output'], list):
            raise JSONRPC(message='Invalid output')

        return result['output']

