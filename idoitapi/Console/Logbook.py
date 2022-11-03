from typing import List

from idoitapi.Console.Console import Console


class Logbook(Console):
    """
    Requests for API namespace 'console.logbook'
    """

    def archive(self) -> List[str]:
        """
        Archive old logbook entries

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.logbook.archive'
        )
