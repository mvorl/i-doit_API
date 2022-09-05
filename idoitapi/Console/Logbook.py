"""
Requests for API namespace 'console.logbook'
"""

from idoitapi.Console.Console import Console


class Logbook(Console):

    def archive(self):
        """
        Archive old logbook entries

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.logbook.archive'
        )
