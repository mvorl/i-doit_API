"""
Requests for API namespace 'cmdb.object_type_categories'
"""

from idoitapi.Request import Request


class CMDBObjectTypeCategories(Request):

    def read(self, object_type):
        """
        Fetch assigned categories for a specific object type by its identifier or constant

        :param object_type: Object type identifier or constant  as integer or string
        :type object_type: int or str
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

    def read_by_id(self, object_type):
        """
        Fetch assigned categories for a specific object type by its identifier

        :param int object_type: Object type identifier
        :return: categories
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_type)

    def read_by_const(self, object_type):
        """
        Fetch assigned categories for a specific object type by its constant

        :param str object_type: Object type constant
        :return: categories
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_type)

    def batch_read(self, object_types):
        """
        Fetches assigned categories for one or more objects types at once
        identified by their identifiers or constants

        :param object_types: List of object types identifiers or constants
        :type object_types: list(int or str)
        :return: Result
        :rtype: list
        """
        requests = list()

        for object_type in object_types:
            requests.append({
                'method': 'cmdb.object_type_categories.read',
                'params': {
                    'type': object_type
                }
            })

        return self._api.batch_request(requests)

    def batch_read_by_id(self, object_types):
        """
        Fetches assigned categories for one or more objects types at once
        identified by their identifiers

        :param object_types: List of object types constants as integer
        :type object_types: list(int)
        :return: Result
        :rtype: list
        """
        return self.read(object_types)

    def batch_read_by_const(self, object_types):
        """
        Fetches assigned categories for one or more objects types at once
        identified by their constants

        :param object_types: List of object types constants as string
        :type object_types: list(str)
        :return: Result
        :rtype: list
        """
        return self.read(object_types)
