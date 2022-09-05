"""
Requests for API namespace 'console.report'
"""

from idoitapi.Console.Console import Console


class Report(Console):

    def export(self, options=None):
        """
        Export report as file

        :param dict options: Options
        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.report.export',
            options
        )
