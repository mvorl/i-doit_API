"""
Requests for API namespace 'console.system'
"""

from idoitapi.Console.Console import Console


class System(Console):

    def purge_unfinished_objects(self):
        """
        Purge unfinished objects

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 1
            }
        )

    def purge_archived_objects(self):
        """
        Purge archived objects

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 3
            }
        )

    def purge_deleted_objects(self):
        """
        Purge deleted objects

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 4
            }
        )
