from typing import List, Dict

from idoitapi.Request import Request


class CMDBObjectTypes(Request):
    """
    Requests for API namespace 'cmdb.object_types'
    """

    def read(self) -> List[Dict]:
        """
        Fetch information about all object types

        :return: list of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.object_types',
            {
                'countobjects': True
            }
        )

    def read_one(self, object_type: str) -> Dict:
        """
        Fetch information about an object type by its constant

        :param str object_type: Object type constant
        :return: object type information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        result = self._api.request(
            'cmdb.object_types',
            {
                'filter': {
                    'id': object_type
                },
                'countobjects': True
            }
        )
        return result[-1] if len(result) >= 1 else None

    def batch_read(self, object_types: List[str]) -> List[Dict]:
        """
        Fetch information about one or more object types by their constants

        :param object_types: List of object type constants as strings
        :type object_types: list[str]
        :return: object types' information
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.object_types',
            {
                'filter': {
                    'ids': object_types
                },
                'countobjects': True
            }
        )

    def read_by_title(self, title: str) -> Dict:
        """
        Fetch information about an object type by its title
        (which could be a "language constant")

        :param str title: Object title
        :return: object type information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.object_types',
            {
                'filter': {
                    'title': title
                },
                'countobjects': True
            }
        )
