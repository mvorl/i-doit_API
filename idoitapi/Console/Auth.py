"""
Requests for API namespace 'console.auth'
"""

from idoitapi.Console.Console import Console


class Auth(Console):

    def cleanup(self):
        """
        Cleanup all auth paths

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.auth.cleanup'
        )
