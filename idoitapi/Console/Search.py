"""
Requests for API namespace 'console.search'
"""

from idoitapi.Console.Console import Console


class Search(Console):

    def create_index(self):
        """
        Create search index from scratch

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.index'
        )

    def update_index(self):
        """
        Update existing search index

        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.index',
            {
                'update': True
            }
        )

    def search(self, query):
        """
        Search for query

        :param query: Query
        :return: Output (one value per line)
        :rtype: list(str)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.query',
            {
                'searchString': query
            }
        )
