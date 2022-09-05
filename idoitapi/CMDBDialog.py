"""
Requests for API namespace 'cmdb.dialog'
"""

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class CMDBDialog(Request):

    def create(self, category, attribute, value, parent=None):
        """
        Create a new entry for a drop-down menu

        :param str category: Category constant
        :param str attribute: Attribute
        :param value: Value
        :param parent: Reference parent entry by its title (string) or by its identifier (integer)
        :type parent: str or int
        :return: Entry identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'category': category,
            'property': attribute,
            'value': value
        }
        if parent is not None:
            params['parent'] = parent

        result = self._api.request(
            'cmdb.dialog.create',
            params
        )

        if 'entry_id' not in result or not isinstance(result['entry_id'], int):
            raise JSONRPC(message='Bad result')

        return result['entry_id']

    def batch_create(self, values):
        """
        Create one or more entries for a drop-down menu

        :param dict values: Values, key is category constant, value is a dict of attribute, value pairs
        :return: List of entry identifiers
        :rtype: list(int)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        requests = []

        for category, key_value_pair in values.items():
            for attribute, mixed in key_value_pair.items():
                if isinstance(mixed, list):
                    attrs = mixed
                else:
                    attrs = [mixed, ]

                for value in attrs:
                    requests.append({
                        'method': 'cmdb.dialog.create',
                        'params': {
                            'category': category,
                            'property': attribute,
                            'value': value
                        }
                    })

        entries = self._api.batch_request(requests)

        entry_ids = []

        for entry in entries:
            if 'entry_id' not in entry or not isinstance(entry['entry_id'], int):
                raise JSONRPC(message='Bad result')
            entry_ids.append(entry['entry_id'])

        return entry_ids

    def read(self, category, attribute):
        """
        Fetch values from drop-down menu

        :param str category: Category constant
        :param str attribute: Attribute
        :return: values
        :rtype: list(dict)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.dialog.read',
            {
                'category': category,
                'property': attribute
            }
        )

    def batch_read(self, attributes):
        """
        Fetch values from one or more drop-down menus

        :param dict attributes: Dict with category constant keys, and attribute name(s) values
        :return: values
        :rtype: list(dict)
        """
        requests = list()

        for category, mixed in attributes.items():
            if isinstance(mixed, list):
                attrs = mixed
            else:
                attrs = [mixed, ]
            for attribute in attrs:
                requests.append({
                    'method': 'cmdb.dialog.read',
                    'params': {
                        'category': category,
                        'property': attribute
                    }
                })

        return self._api.batch_request(requests)

    def delete(self, category, attribute, entry_id):
        """
        Purge value from drop-down menu

        :param str category: Category constant
        :param str attribute: Attribute
        :param int entry_id: Entry identifier
        :return: self
        :rtype: object
        """
        self._api.request(
            'cmdb.dialog.delete',
            {
                'category': category,
                'property': attribute,
                'entry_id': entry_id
            }
        )
