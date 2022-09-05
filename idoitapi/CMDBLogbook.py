"""
Requests for API namespace 'cmdb.logbook'
"""

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class CMDBLogbook(Request):

    def create(self, object_id, message, description=None):
        """
        Create a new logbook entry

        :param int object_id: Object identifier
        :param str message: Message
        :param str description: (optional) Description
        :return: self
        :rtype: object
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

        return self

    def batch_create(self, object_id, messages):
        """
        Create one or more logbook entries for a specific object

        :param int object_id: Object identifier
        :param messages: List of messages as strings
        :type messages: list(str)
        :return: self
        :rtype: object
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

        return self

    def read(self, since=None, limit=1000):
        """
        Fetch all logbook entries

        :param str since: (optional) list only entries since a specific date;
          supports everything which can be parsed by PHP's
          `strtotime() <https://www.php.net/manual/en/function.strtotime.php>`_
        :param int limit: Limit number of entries
        :return: List of dicts
        :rtype: list(dict)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'limit': limit,
        }

        if since is not None:
            params['since'] = since

        return self._api.request(
            'cmdb.logbook.read',
            params,
        )

    def read_by_object(self, object_id, since=None, limit=1000):
        """
        Fetch all logbook entries for a specific object

        :param int object_id: Object identifier
        :param str since: (optional) list only entries since a specific date;
          supports everything which can be parsed by PHP's
          `strtotime() <https://www.php.net/manual/en/function.strtotime.php>`_
        :param int limit: Limit number of entries
        :return: List of dicts
        :rtype: list(dict)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'object_id': object_id,
            'limit': limit,
        }

        if since is not None:
            params['since'] = since

        return self._api.request(
            'cmdb.logbook.read',
            params,
        )
