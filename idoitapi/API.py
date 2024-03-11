import json
from typing import Dict, Any, List, Optional

import requests
from idoitapi.APIException import JSONRPC, InvalidParams, InternalError, MethodNotFound, UnknownError

# Values for User-Agent header
# ToDo: Grab User-Agent name from setup.py
API_AGENT_NAME = 'idoitapi' + '-python'
API_AGENT_VERSION = '1.0b7'
API_AGENT_COMMENT = ''


class API(object):
    """
    Low-Level object to access the i-doit JSON-RPC API.
    """

    def __init__(self,
                 url: str,
                 key: str,
                 language: Optional[str] = None,
                 username: Optional[str] = None,
                 password: Optional[str] = None
                 ) -> None:
        """
        If username and password are not given, 'System API' user will be used.

        :param str url: Base URL to i-doit's API
        :param str key: API Key
        :param str language: requests to and responses from i-doit will be translated
            to this language ('de' and 'en' supported)
        :param str username: (optional) Username
        :param str password: (optional) Password
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if not isinstance(url, str) or url == '':
            raise InvalidParams(message='URL parameter is invalid')
        if not (url.startswith('http://') or url.startswith('https://')):
            raise InvalidParams(message='Unsupported protocol in API URL '+url)

        if not isinstance(key, str) or key == '':
            raise InvalidParams(message='API key parameter is invalid')

        if username is not None:
            if not isinstance(username, str) or username == '':
                raise InvalidParams(message='username parameter is invalid')
            if password is None:
                raise InvalidParams(message='Username has no password')
            else:
                if not isinstance(password, str) or password == '':
                    raise InvalidParams(message='password parameter is invalid')
        elif password is not None:
            raise InvalidParams(message='There is no username')

        if language is not None:
            if language not in ('de', 'en'):
                raise InvalidParams(message='language parameter is invalid')

        if url.endswith('/src/jsonrpc.php'):
            self.url = url
        else:
            if not url.endswith('/'):
                url += '/'
            self.url = url + 'src/jsonrpc.php'
        self.key = key
        self.username = username
        self.password = password
        self._language = language
        self._session_id = None
        self._id = 0

    # def __del__(self):
    #     """
    #     Destructor automatically logs out from API if necessary
    #     """
    #     try:
    #         if self.is_logged_in():
    #             self.logout()
    #     except APIException:
    #         pass  # Do nothing because this is a destructor.

    def is_logged_in(self) -> bool:
        """
        Check whether API is logged in

        :return: ``True`` if logged in
        :rtype: bool
        """
        return self._session_id is not None

    def login(self, username: Optional[str] = None, password: Optional[str] = None) -> None:
        """
        Login to API.

        :param str username: Overrides the current username value
        :param str password: Overrides the current password value
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password

        headers = {
            'X-RPC-Auth-Username': self.username,
            'X-RPC-Auth-Password': self.password
        }

        response = self.request(
            'idoit.login',
            headers=headers
        )
        self._session_id = response['session-id']

    def logout(self) -> None:
        """
        Logout from API.

        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self.request('idoit.logout')
        self._session_id = None

    def generate_id(self) -> int:
        """
        Generate new JSON-RPC request identifier

        :return: the next request identifier
        :rtype: int
        """
        self._id += 1
        return self._id

    def count_request(self) -> int:
        """
        How many requests were already sent?

        :return: Number of requests
        :rtype: int
        """
        return self._id

    def request(self, method: str, params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Any:
        """
        Perform a JSON RPC request.

        :param str method: JSON RPC API method name
        :param dict params: method parameters
        :param dict headers: additional header lines
        :return: the method's output data
        :rtype: Any
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        req_headers = {
            'Content-Type': 'application/json',
            'User-Agent': API_AGENT_NAME + '/' + API_AGENT_VERSION + ' ' + API_AGENT_COMMENT
        }
        if self._session_id is not None:
            req_headers['X-RPC-Auth-Session'] = self._session_id

        if isinstance(headers, dict):
            req_headers.update(headers)

        req_params = {
            'apikey': self.key
        }
        if isinstance(params, dict):
            req_params.update(params)
        if self._language is not None and 'language' not in req_params:
            req_params['language'] = self._language

        payload = {
            'version': '2.0',
            'method': method,
            'params': req_params,
            'id': self.generate_id(),
        }

        response = requests.post(
            self.url,
            data=json.dumps(payload),
            headers=req_headers
        ).json()

        if 'error' in response:
            error = response['error']
            error_code = error['code']
            for exception_class in [InvalidParams, InternalError, MethodNotFound]:
                if exception_class.code == error_code:
                    raise exception_class(
                        data=error['data'],
                        raw_code=error_code,
                        message=error['message']
                    )
            raise UnknownError(
                data=error['data'],
                raw_code=error_code,
                message=error['message']
            )

        return response['result']

    def batch_request(self, payload: List[Dict], headers: Optional[Dict] = None) -> List[Any]:
        """
        Perform a JSON RPC batch request.

        :param list[dict] payload: list of requests,
            each with 'method' key, and optionally 'params' and 'id'
        :param dict headers: additional header lines
        :return: list of response data, each with either a 'result' or an 'error' key
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        req_headers = {
            'content-type': 'application/json'
        }
        if self._session_id is not None:
            req_headers['X-RPC-Auth-Session'] = self._session_id

        if isinstance(headers, dict):
            req_headers.update(headers)

        data = []

        for rq in payload:
            if 'method' not in rq:
                raise JSONRPC(message='Missing method in one of the sub-requests of this batch request')

            params = {}

            if 'params' in rq:
                params = rq['params']

            params['apikey'] = self.key
            if self._language is not None and 'language' not in rq:
                params['language'] = self._language
            if 'id' not in rq:
                rq['id'] = self.generate_id()

            data.append({
                'version': '2.0',
                'method': rq['method'],
                'params': params,
                'id': rq['id']
            })

        responses = requests.post(
            self.url,
            data=json.dumps(data),
            headers=req_headers
        ).json()

        results = []

        for response in responses:
            if not isinstance(response, dict):
                raise JSONRPC(message='Found invalid result for request in batch: {}'.format(response))
            if 'error' in response:
                results.append(response['error'])
            else:
                results.append(response['result'])

        return results
