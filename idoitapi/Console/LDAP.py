from typing import List, Dict

from idoitapi.Console.Console import Console


class LDAP(Console):
    """
    Requests for API namespace 'console.ldap'
    """

    def sync(self, ldap_server_id: int) -> List[str]:
        """
        Synchronize LDAP user accounts with i-doit person objects

        :param int ldap_server_id: Identifier of LDAP configuration
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.sync',
            {
                'ldapServerId': ldap_server_id
            }
        )

    def sync_all(self) -> List[str]:
        """
        Synchronize LDAP user accounts with i-doit person objects

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.sync'
        )

    def sync_distinguished_names(self, options: Dict = None) -> List[str]:
        """
        Synchronize distinguished names (DN) from LDAP user accounts with
        i-doit person objects

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.syncdn',
            options
        )
