from typing import Union, List

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC
from idoitapi.CMDBObjects import CMDBObjects
from idoitapi.CMDBCategory import CMDBCategory


class Select(Request):
    """
    Selector for objects
    """

    def find(self, category: str, attribute: str, value: Union[int, str, float]) -> List[int]:
        """
        Find objects by attribute

        :param str category: a category string
        :param str attribute: an attribute name
        :param value: an attribute value
        :type value: Union[int, str, float]
        :return: List of object identifiers as integers
        :rtype: List[int]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if value is None:
            raise JSONRPC(message='value can not be None')

        cmdb_objects = CMDBObjects(self._api)

        limit = 100
        offset = 0

        object_ids = []

        while True:
            objects = cmdb_objects.read(limit=limit, offset=offset)

            count = len(objects)

            if count == 0:
                break

            result = CMDBCategory(self._api).batch_read(
                [int(obj['id']) for obj in objects],
                [category, ]
            )

            for categoryEntries in result:
                for categoryEntry in categoryEntries:
                    if attribute in categoryEntry:
                        item = categoryEntry[attribute]

                        if (
                            (isinstance(item, dict) and
                             (item.get('ref_title') == value or item.get('title') == value))
                                or
                            (isinstance(item, (int, float, str)) and item == value)
                        ):

                            if 'objID' not in categoryEntry:
                                raise JSONRPC(message='Found attribute for unknown object')

                            object_ids.append(int(categoryEntry['objID']))

            if count < limit:
                break

            offset += limit

        return object_ids
