from typing import List, Union, Any

from idoitapi.Request import Request


class CMDBObjectTypeCategories(Request):
    """
    Requests for API namespace 'cmdb.object_type_categories'
    """

    def read(self, object_type: Union[int, str]) -> List:
        """
        Fetch assigned categories for a specific object type by its identifier or constant

        :param object_type: Object type identifier or constant as integer or string
        :type object_type: Union[int, str]
        :return: categories
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            method='cmdb.object_type_categories.read',
            params={
                'type': object_type
            }
        )

    def read_by_id(self, object_type: int) -> List:
        """
        Fetch assigned categories for a specific object type by its identifier

        :param int object_type: Object type identifier
        :return: categories
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_type)

    def read_by_const(self, object_type: str) -> List:
        """
        Fetch assigned categories for a specific object type by its constant

        :param str object_type: Object type constant
        :return: categories
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_type)

    def batch_read(self, object_types: Union[List[int], List[str]]) -> List[Any]:
        """
        Fetches assigned categories for one or more objects types at once
        identified by their identifiers or constants

        :param object_types: List of object types identifiers or constants
        :type object_types: List[Union[int, str]]
        :return: Result
        :rtype: list
        """
        requests = []

        for object_type in object_types:
            requests.append({
                'method': 'cmdb.object_type_categories.read',
                'params': {
                    'type': object_type
                }
            })

        return self._api.batch_request(requests)

    def batch_read_by_id(self, object_types: List[int]) -> List[Any]:
        """
        Fetches assigned categories for one or more objects types at once
        identified by their identifiers

        :param object_types: List of object types constants as integer
        :type object_types: list[int]
        :return: Result
        :rtype: list
        """
        return self.batch_read(object_types)

    def batch_read_by_const(self, object_types: List[str]) -> List[Any]:
        """
        Fetches assigned categories for one or more objects types at once
        identified by their constants

        :param object_types: List of object types constants as string
        :type object_types: List[str]
        :return: Result
        :rtype: list
        """
        return self.batch_read(object_types)
