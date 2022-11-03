from typing import List

from idoitapi.Console.Console import Console


class Auth(Console):
    """
    Requests for API namespace 'console.auth'
    """

    def cleanup(self) -> List[str]:
        """
        Cleanup all auth paths

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.auth.cleanup'
        )
