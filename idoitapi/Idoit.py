from typing import Any, List, Dict

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class Idoit(Request):
    """
    Requests for API namespace 'idoit'
    """

    @property
    def version(self) -> str:
        """
        Fetch the i-doit version

        :return: version number
        :rtype: str
        """
        data = self.read_version()
        return data['version']

    @property
    def version_type(self) -> str:
        """
        Fetch the i-doit version type

        :return: version type
        :rtype: str
        """
        data = self.read_version()
        return data['type']

    def read_version(self) -> Dict:
        """
        Read information about i-doit

        :return: information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request('idoit.version')

    def get_addons(self) -> List[Any]:
        """
        Read information about installed add-ons

        :return: information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        response = self._api.request('idoit.addons.read')

        if 'result' not in response or not isinstance(response['result'], list):
            raise JSONRPC(message='Bad result')

        return response['result']

    def get_license(self) -> Dict:
        """
        Read license information

        :return: license information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request('idoit.license.read')

    def read_constants(self) -> Dict:
        """
        Read list of defined constants

        :return: information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request('idoit.constants')

    def search(self, query: str) -> Any:
        """
        Search i-doit's database

        :param str query: Query
        :return: Search results
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'idoit.search',
            {
                'q': query
            }
        )

    def batch_search(self, queries: List[str]) -> Any:
        """
        Perform one or more searches at once

        :param list[str] queries: Queries as strings
        :return: Search results
        """
        requests = []

        for query in queries:
            requests.append({
                'method': 'idoit.search',
                'params': {
                    'q': query
                }
            })

        return self._api.batch_request(requests)
