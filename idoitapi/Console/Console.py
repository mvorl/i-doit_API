"""
Requests for API namespace 'console'
"""

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class Console(Request):

    def execute(self, method, options=None, arguments=None):
        """
        Execute command

        :param str method: Method name
        :param dict options: List of options as key-value store
        :param arguments: List of arguments as strings
        :type arguments: list(str)
        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {}

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

