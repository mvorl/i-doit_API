"""
Requests for API namespace 'cmdb.workstation_components'
"""

from idoitapi.Request import Request


class CMDBWorkstationComponents(Request):

    def read(self, object_id):
        """
        Reads workplace components for a specific object, for example a person

        :param int object_id: Object identifier
        :return: result
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.workstation_components',
            {
                filter: {
                    'id': object_id,
                }
            }
        )

    def batch_read(self, object_ids):
        """
        Reads workplace components for one or more objects, for example persons

        :param object_ids: List of object identifiers as integers
        :type object_ids: list(int)
        :return: result
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.workstation_components',
            {
                filter: {
                    'ids': object_ids,
                }
            }
        )

    def read_by_email(self, email):
        """
        Reads workplace components for a specific object by its e-mail address, for example a person

        :param str email: E-mail address
        :return: result
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.workstation_components',
            {
                filter: {
                    'email': email,
                }
            }
        )

    def read_by_emails(self, emails):
        """
        Reads workplace components for one or more objects by their e-mail addresses, for example persons

        :param emails: List of e-mail addresses as strings
        :type emails: list(str)
        :return: result
        :rtype: list
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.workstation_components',
            {
                filter: {
                    'emails': emails,
                }
            }
        )
