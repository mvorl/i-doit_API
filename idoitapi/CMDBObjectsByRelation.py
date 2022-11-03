from typing import Union, List

from idoitapi.Request import Request


class CMDBObjectsByRelation(Request):
    """
    Requests for API namespace 'cmdb.objects_by_relation'
    """

    def read(self, object_id: int, relation_type: Union[int, str], status: int = None) -> List:
        """
        Read object relations by their type identifier or constant

        :param int object_id: Object identifier
        :param relation_type: Relation type identifier or constant
        :type relation_type:  Union[int, str]
        :param int status: (optional) Filter relations by status:
            2 = normal, 3 = archived, 4 = deleted
        :return: values
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'id': object_id,
            'relation_type': relation_type
        }

        if status is not None:
            params['status'] = status

        return self._api.request(
            method='cmdb.objects_by_relation.read',
            params=params
        )

    def read_by_id(self, object_id: int, relation_type: int, status: int = None) -> List:
        """
        Read object relations by their type identifier

        :param int object_id: Object identifier
        :param int relation_type: Relation type identifier
        :param int status: (optional) Filter relations by status:
            2 = normal, 3 = archived, 4 = deleted
        :return: values
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
         """
        return self.read(object_id, relation_type, status)

    def read_by_const(self, object_id: int, relation_type: str, status: int = None) -> List:
        """
        Read object relations by their type constant

        :param int object_id: Object identifier
        :param str relation_type: Relation type constant
        :param int status: (optional) Filter relations by status:
            2 = normal, 3 = archived, 4 = deleted
        :return: values
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.read(object_id, relation_type, status)
