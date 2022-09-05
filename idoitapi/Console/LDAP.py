"""
Requests for API namespace 'console.ldap'
"""

from idoitapi.Console.Console import Console


class LDAP(Console):

    def sync(self, ldap_server_id):
        """
        Synchronize LDAP user accounts with i-doit person objects

        :param int ldap_server_id: Identifier of LDAP configuration
        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.sync',
            {
                'ldapServerId': ldap_server_id
            }
        )

    def sync_all(self):
        """
        Synchronize LDAP user accounts with i-doit person objects

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.sync'
        )

    def sync_distinguished_names(self, options=None):
        """
        Synchronize distinguished names (DN) from LDAP user accounts with
        i-doit person objects

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.ldap.syncdn',
            options
        )
