from typing import Union, List, Any

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class CMDBImpact(Request):
    """
    Requests for API namespace 'cmdb.impact'
    """

    def read(self, object_id: int, relation_type: Union[int, str, List[Union[int, str]]], status: int = None) -> Any:
        """
        Perform an impact analysis for a specific object by its relation type identifier or constant

        :param int object_id: Object identifier
        :param relation_type: Relation type identifier or constant or list of these
        :type relation_type: int or str or list(int or str)
        :param int status: Filter relations by status: 2 = normal, 3 = archived, 4 = deleted
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'id': object_id,
            'relation_type': relation_type
        }
        if status is not None:
            params['status'] = status

        return self._api.request(
            'cmdb.impact.read',
            params
        )

    def read_by_id(self, object_id: int, relation_type: int, status: int = None) -> Any:
        """
        Perform an impact analysis for a specific object by its relation type identifier

        :param int object_id: Object identifier
        :param int relation_type: Relation type identifier
        :param int status: Filter relations by status: 2 = normal, 3 = archived, 4 = deleted
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_id, relation_type, status)

    def read_by_const(self, object_id: int, relation_type: str, status: int = None) -> Any:
        """
        Perform an impact analysis for a specific object by its relation type constant

        :param int object_id: Object identifier
        :param str relation_type: Relation type constant
        :param int status: Filter relations by status: 2 = normal, 3 = archived, 4 = deleted
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_id, relation_type, status)

    def read_by_types(self, object_id: int, relation_types: List[Union[int, str]], status: int = None) -> Any:
        """
        Perform an impact analysis for a specific object by one ore more relation type constant or identifiers

        :param int object_id: Object identifier
        :param List[Union[int, str]] relation_types: List of relation type constants
            as strings or identifiers as integers
        :param int status: Filter relations by status: 2 = normal, 3 = archived, 4 = deleted
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_id, relation_types, status)
