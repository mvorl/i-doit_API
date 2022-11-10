from typing import List, Dict, Union

from idoitapi.Request import Request
# from idoitapi.APIException import JSONRPC


class CMDBStatus(Request):
    """
    Requests for API namespace 'cmdb.status'
    """

    ATTRIBUTE_ID = 'id'
    ATTRIBUTE_TITLE = 'title'
    ATTRIBUTE_CONSTANT = 'constant'
    ATTRIBUTE_COLOR = 'color'
    ATTRIBUTE_EDITABLE = 'editable'

    def read(self) -> List[Dict]:
        """
        Get list of available CMDB states

        :return: Indexed array of associative arrays
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.status.read'
        )

    def save(self, title: str, constant: str, color: str, identifier: int = None) -> int:
        """
        Create new or update existing CMDB status

        :param str title: Title
        :param str constant: Constant
        :param str color: Color
        :param int identifier: Set identifier to update existing status, otherwise a new one will be created
        :return: Identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Union[str, int]] = {
            self.ATTRIBUTE_TITLE: title,
            self.ATTRIBUTE_CONSTANT: constant,
            self.ATTRIBUTE_COLOR: color,
        }

        if identifier is not None:
            params[self.ATTRIBUTE_ID] = identifier

        result = self._api.request(
            'cmdb.status.save',
            params
        )

        return self.require_success_for(result)

    def delete(self, status_id: int) -> None:
        """
        Purge CMDB status from database

        :param int status_id: Identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        result = self._api.request(
            'cmdb.status.delete',
            {
                self.ATTRIBUTE_ID: status_id
            }
        )

        self.require_success_without_identifier(result)
