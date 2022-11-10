from typing import List, Dict, Union

from idoitapi.Request import Request


class CMDBLogbook(Request):
    """
    Requests for API namespace 'cmdb.logbook'
    """

    def create(self, object_id: int, message: str, description: str = None) -> None:
        """
        Create a new logbook entry

        :param int object_id: Object identifier
        :param str message: Message
        :param str description: (optional) Description
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'object_id': object_id,
            'message': message,
        }

        if description is not None:
            params['description'] = description

        result = self._api.request(
            'cmdb.logbook.create',
            params,
        )

        self.require_success_without_identifier(result)

    def batch_create(self, object_id: int, messages: List[str]) -> None:
        """
        Create one or more logbook entries for a specific object

        :param int object_id: Object identifier
        :param messages: List of messages as strings
        :type messages: list[str]
        """
        requests = []

        for message in messages:
            requests.append({
                'method': 'cmdb.logbook.create',
                'params': {
                    'object_id': object_id,
                    'message': message,
                }
            })

        self._api.batch_request(requests)

    def read(self, since: str = None, limit: int = 1000) -> List[Dict]:
        """
        Fetch all logbook entries

        :param str since: (optional) list only entries since a specific date;
          supports everything which can be parsed by PHP's
          `strtotime() <https://www.php.net/manual/en/function.strtotime.php>`_
        :param int limit: (optional) Limit number of entries; default: 1000
        :return: List of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Union[str, int]] = {
            'limit': limit,
        }

        if since is not None:
            params['since'] = since

        return self._api.request(
            'cmdb.logbook.read',
            params,
        )

    def read_by_object(self, object_id: int, since: str = None, limit: int = 1000) -> List[Dict]:
        """
        Fetch all logbook entries for a specific object

        :param int object_id: Object identifier
        :param str since: (optional) list only entries since a specific date;
          supports everything which can be parsed by PHP's
          `strtotime() <https://www.php.net/manual/en/function.strtotime.php>`_
        :param int limit: (optional) Limit number of entries; default: 1000
        :return: List of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Union[str, int]] = {
            'object_id': object_id,
            'limit': limit,
        }

        if since is not None:
            params['since'] = since

        return self._api.request(
            'cmdb.logbook.read',
            params,
        )
