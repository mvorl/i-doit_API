from typing import List

from idoitapi.Console.Console import Console


class System(Console):
    """
    Requests for API namespace 'console.system'
    """

    def purge_unfinished_objects(self) -> List[str]:
        """
        Purge unfinished objects

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 1
            }
        )

    def purge_archived_objects(self) -> List[str]:
        """
        Purge archived objects

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 3
            }
        )

    def purge_deleted_objects(self) -> List[str]:
        """
        Purge deleted objects

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.system.objectcleanup',
            {
                'objectStatus': 4
            }
        )
