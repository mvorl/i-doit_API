from typing import Any

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class CMDBLocationTree(Request):
    """
    Requests for API namespace 'cmdb.location_tree'
    """

    def read(self, object_id: int, status: int = None) -> Any:
        """
        Reads objects located directly under an object

        This method does not run recursively. Use read_recursively() instead.

        :param int object_id: Object identifier
        :param int status: (optional) Filter relations by status:
            2 = normal, 3 = archived, 4 = deleted
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'id': object_id
        }
        if status is not None:
            params['status'] = status

        return self._api.request(
            'cmdb.location_tree.read',
            params
        )

    def read_recursively(self, object_id: int, status: int = None, level: int = -1) -> Any:
        """
        Reads recursively objects located under an object

        :param int object_id: Object identifier
        :param int status: (optional) Filter relations by status:
            2 = normal, 3 = archived, 4 = deleted
        :param int level: (optional) Level of recursion; negative values for no limit;
            default: no Limit
        :return: array
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        children = self.read(object_id, status)

        tree = list()

        if level != 0:
            for child in children:
                if 'id' not in child:
                    raise JSONRPC(message='Broken result')

                node = dict(child)

                child_children = self.read_recursively(child['id'], status, level-1)

                if len(child_children) > 0:
                    node['children'] = child_children

                tree.append(node)

        return tree
