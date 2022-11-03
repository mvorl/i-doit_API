from typing import List

from idoitapi.Console.Console import Console


class Notifications(Console):
    """
    Requests for API namespace 'console.notifications'
    """

    def send(self) -> List[str]:
        """
        Send e-mail notifications

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.notifications.send'
        )
