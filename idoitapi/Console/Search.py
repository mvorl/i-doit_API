from typing import List

from idoitapi.Console.Console import Console


class Search(Console):
    """
    Requests for API namespace 'console.search'
    """

    def create_index(self) -> List[str]:
        """
        Create search index from scratch

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.index'
        )

    def update_index(self) -> List[str]:
        """
        Update existing search index

        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.index',
            {
                'update': True
            }
        )

    def search(self, query: str) -> List[str]:
        """
        Search for query

        :param str query: Query
        :return: Output (one value per line)
        :rtype: list[str]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self.execute(
            'console.search.query',
            {
                'searchString': query
            }
        )
