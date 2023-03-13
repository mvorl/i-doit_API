from typing import List, Dict, Optional

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC


class CMDBCategory(Request):
    """
    Requests for API namespace 'cmdb.category'
    """

    def save(self, object_id: int, category: str, attributes: Dict, entry_id: Optional[int] = None) -> int:
        """
        Create new or update existing category entry for a specific object.
        Suitable for single- and multi-value categories.

        :param int object_id: Object identifier
        :param str category: Category constant
        :param dict attributes: Attributes
        :param int entry_id: Entry identifier (only needed for multi-valued categories)
        :return: Entry identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'object': object_id,
            'category': category,
            'data': attributes,
        }
        if entry_id is not None:
            params['entry'] = entry_id

        result = self._api.request(
            'cmdb.category.save',
            params
        )

        if 'entry' not in result or not isinstance(result['entry'], int) \
                or 'success' not in result or not result['success']:
            message = 'Bad result'
            if 'message' in result:
                message += ': ' + result['message']
            raise JSONRPC(message=message)

        return result['entry']

    def create(self, object_id: int, category: str, attributes: Dict) -> int:
        """
        Create new category entry for a specific object.

        :param int object_id: Object identifier
        :param str category: Category constant
        :param dict attributes: Attributes
        :return: Entry identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'objID': object_id,
            'category': category,
            'data': attributes,
        }

        result = self._api.request(
            'cmdb.category.create',
            params
        )

        return self.require_success_for(result)

    def read(self, object_id: int, category: str, status: int = 2) -> List[Dict]:
        """
        Read one or more category entries for a specific object
        (works with both single- and multi-valued categories).

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int status: Filter entries by status:
            2 = normal,
            3 = archived,
            4 = deleted,
            -1 = combination of all;
            defaults to: 2 = normal;
            note: a status != 2 is only suitable for multi-value categories
        :return: List of result sets (for both single- and multi-valued categories)
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.category.read',
            {
                'objID': object_id,
                'category': category,
                'status': status
            }
        )

    def read_one_by_id(self, object_id: int, category: str, entry_id: int, status: int = 2) -> Dict:
        """
        Read one specific category entry for a specific object
        (works with both single- and multi-valued categories)

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier
        :param int status: Filter entries by status:
            2 = normal,
            3 = archived,
            4 = deleted,
            -1 = combination of all;
            defaults to: 2 = normal;
            note: a status != 2 is only suitable for multi-value categories
        :return: category entry
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        entries = self.read(object_id, category, status)

        for entry in entries:
            if 'id' not in entry:
                raise JSONRPC(
                    message='Entries for category "{}" contain no identifier'.format(category)
                )
            if int(entry['id']) == entry_id:
                return entry
        else:
            raise JSONRPC(
                message='No entry with identifier {} found in category "{}" for object {}'.format(
                    entry_id, category, object_id
                )
            )

    def read_first(self, object_id: int, category: str) -> Dict:
        """
        Read first category entry for a specific object
        (works with both single- and multi-valued categories)

        :param int object_id: Object identifier
        :param str category: Category constant
        :return: category entry, otherwise empty dict when there is no entry
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        entries = self.read(object_id, category)
        if len(entries) == 0:
            return dict()
        return entries[0]

    def update(self, object_id: int, category: str, attributes: Dict, entry_id: Optional[int] = None) -> None:
        """
        Update category entry for a specific object

        :param int object_id: Object identifier
        :param str category: Category constant
        :param dict attributes: Attributes
        :param int entry_id: Entry identifier (only needed for multi-valued categories)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if entry_id is not None:
            attributes['category_id'] = entry_id

        result = self._api.request(
            'cmdb.category.update',
            {
                'objID': object_id,
                'category': category,
                'data': attributes
            }
        )

        self.require_success_without_identifier(result)

    def archive(self, object_id: int, category: str, entry_id: int) -> None:
        """
        Archive entry in a multi-value category for a specific object

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.category.archive',
            {
                'objID': object_id,
                'category': category,
                'entry': entry_id
            }
        )

    def delete(self, object_id: int, category: str, entry_id: int) -> None:
        """
        Marks entry in a multi-value category for a specific object as deleted

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.category.delete',
            {
                'objID': object_id,
                'category': category,
                'entry': entry_id
            }
        )

    def purge(self, object_id: int, category: str, entry_id: Optional[int] = None) -> None:
        """
        Purge entry in a single- or multi-value category for a specific object

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier (only needed for multi-value categories)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'object': object_id,
            'category': category,
        }

        if entry_id is not None:
            params['entry'] = entry_id

        self._api.request(
            'cmdb.category.purge',
            params
        )

    def recycle(self, object_id: int, category: str, entry_id: int) -> None:
        """
        Restore entry in a multi-value category for a specific object to "normal" state

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.category.recycle',
            {
                'objID': object_id,
                'category': category,
                'entry': entry_id
            }
        )

    def quick_purge(self, object_id: int, category: str, entry_id: int) -> None:
        """
        Purge entry in a multi-value category for a specific object

        :param int object_id: Object identifier
        :param str category: Category constant
        :param int entry_id: Entry identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        # noinspection SpellCheckingInspection
        result = self._api.request(
            'cmdb.category.quickpurge',
            {
                'objID': object_id,
                'category': category,
                'entry': entry_id
            }
        )

        self.require_success_without_identifier(result)

    def batch_create(self, object_ids: List[int], category: str, attributes: List[Dict]) -> List[int]:
        """
        Create multiple entries for a specific category and one or more objects

        :param list[int] object_ids: List of object identifiers as integers
        :param str category: Category constant
        :param list[dict] attributes: attributes
        :return: List of entry identifiers as integers
        :rtype: list[int]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        entry_ids = []

        requests = []

        for object_id in object_ids:
            for data in attributes:
                requests.append({
                    'method': 'cmdb.category.create',
                    'params': {
                        'objID': object_id,
                        'category': category,
                        'data': data
                    }
                })

        results = self._api.batch_request(requests)

        self.require_success_for_all(results)

        for entry in results:
            entry_ids.append(int(entry['id']))

        return entry_ids

    def batch_read(self, object_ids: List[int], categories: List[str], status: int = 2) -> List[List]:
        """
        Read one or more category entries for one or more objects

        :param List[int] object_ids: List of object identifiers as integers
        :param list[str] categories: List of category constants as strings
        :param int status: Filter entries by status:
            2 = normal,
            3 = archived,
            4 = deleted,
            -1 = combination of all;
            defaults to: 2 = normal;
            note: a status != 2 is only suitable for multi-value categories
        :return: list of result sets (for both single- and multi-valued categories)
        :rtype: list
        """
        if len(object_ids) == 0:
            raise JSONRPC(message='Needed at least one object identifier')
        if len(categories) == 0:
            raise JSONRPC(message='Needed at least one category constant')

        requests = []

        for object_id in object_ids:
            if not isinstance(object_id, int) or object_id <= 0:
                raise JSONRPC(message='Each object identifier must be a positive integer')
            for category in categories:
                if not isinstance(category, str) or category == '':
                    raise JSONRPC(message='Each category constant must be a non-empty string')
                requests.append({
                    'method': 'cmdb.category.read',
                    'params': {
                        'objID': object_id,
                        'category': category,
                        'status': status
                    }
                })

        results = self._api.batch_request(requests)

        expected_amount_of_results = len(object_ids) * len(categories)
        actual_amount_of_results = len(results)

        if expected_amount_of_results != actual_amount_of_results:
            raise JSONRPC(
                message='Requested entries for {} object(s) and {} category/categories but got {} result(s)'.format(
                    len(object_ids),
                    len(categories),
                    actual_amount_of_results
                )
            )

        return results

    def batch_update(self, object_ids: List[int], category: str, attributes: Dict) -> None:
        """
        Update single-value category for one or more objects

        :param list[int] object_ids: List of object identifiers as integers
        :param str category: Category constant
        :param dict attributes: Attributes
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        requests = []

        for object_id in object_ids:
            requests.append({
                'method': 'cmdb.category.create',
                'params': {
                    'objID': object_id,
                    'category': category,
                    'data': attributes
                }
            })

        result = self._api.batch_request(requests)

        self.require_success_for_all(result)

    def clear(self, object_id: int, categories: List[str]) -> int:
        """
        Archive category entries for a specific object

        :param int object_id: Object identifier
        :param list[str] categories: List of category constants as strings
        :return: Number of purged category entries
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        counter = 0

        batch = self.batch_read([object_id], categories)

        requests = []

        for idx, entries in enumerate(batch):
            category = categories[idx]

            for entry in entries:
                requests.append({
                    'method': 'cmdb.category.archive',
                    'params': {
                        'object': object_id,
                        'category': category,
                        'entry': int(entry['id'])
                    }
                })
                counter += 1

        if counter == 0:
            return 0

        results = self._api.batch_request(requests)

        self.require_success_for_all(results)

        return counter
