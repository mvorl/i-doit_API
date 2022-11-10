from typing import List, Union, Dict, Any, Literal

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC, InvalidParams


class CMDBObjects(Request):
    """
    Requests for API namespace 'cmdb.objects'
    """

    SORT_ASCENDING = 'ASC'
    SORT_DESCENDING = 'DESC'

    def create(self, objects: List[Dict]) -> List[int]:
        """
        Create one or more objects

        :param list[dict] objects: List of objects
            Mandatory attributes ('type', 'title') and optional attributes
            ('category', 'purpose', 'cmdb_status', 'description')
        :return: Object identifiers
        :rtype: list[int]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if not isinstance(objects, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(objects) == 0:
            return []

        requests = []

        for obj in objects:
            requests.append({
                'method': 'cmdb.object.create',
                'params': obj
            })

        result = self._api.batch_request(requests)

        return [obj['id'] for obj in result]

    def read(self,
             filter_params: Dict = None,
             limit: int = None,
             offset: int = None,
             order_by: str = None,
             sort: str = None,
             categories: Union[List[str], Literal[True]] = None
             ) -> List[Dict]:
        """
        Fetch objects.

        :param dict filter_params: (optional) Filter;
            use any combination of 'ids' (array of object identifiers),
            'type' (object type identifier), 'type_group', 'status',
            'title' (object title), 'type_title' (l10n object type),
            'location', 'sysid', 'first_name', 'last_name', 'email'
        :param int limit: (optional) Limit result set
        :param int offset: (optional) Offset for limit
        :param str order_by: (optional) Order result set by
            'isys_obj_type__id', 'isys_obj__isys_obj_type__id', 'type',
            'isys_obj__title', 'title', 'isys_obj_type__title', 'type_title',
            'isys_obj__sysid', 'sysid', 'isys_cats_person_list__first_name',
            'first_name', 'isys_cats_person_list__last_name', 'last_name',
            'isys_cats_person_list__mail_address', 'email', 'isys_obj__id', 'id'
        :param str sort: (optional) Sort ascending ('asc') or descending ('desc')
        :param categories: (optional) Also fetch category entries;
            add a list of category constants as strings or
            ``True`` for all assigned categories
        :type categories: union[list[str], True]
        :return: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Any] = {}

        if isinstance(filter_params, dict):
            params['filter'] = filter_params

        if categories is True or isinstance(categories, list):
            params['categories'] = categories

        if limit is not None:
            if not isinstance(limit, int) or limit < 0:
                raise InvalidParams(message='"{}" is not a valid limit parameter'.format(limit))
            if offset is not None:
                if not isinstance(offset, int) or offset < 0:
                    raise InvalidParams(message='"{}" is not a valid offset parameter'.format(offset))
                # noinspection PyTypedDict
                params['limit'] = "{},{}".format(offset, limit)
            else:
                params['limit'] = limit

        if order_by is not None:
            params['order_by'] = order_by

        if sort is not None:
            if sort.lower() not in ('asc', 'desc'):
                raise InvalidParams(message='"{}" is not a valid sort_direction parameter'.format(sort))
            params['sort'] = sort

        return self._api.request(
            'cmdb.objects.read',
            params
        )

    def read_by_ids(self, object_ids: List[int], categories: Union[List[str], Literal[True]] = None) -> List[Dict]:
        """
        Fetch objects by their identifiers.

        :param list object_ids: List of object identifiers as integers
        :param categories: (optional) Also fetch category entries;
            add a list of category constants as strings or
            ``True`` for all assigned categories
        :type categories: Union[List[str], True, None]
        :return: List of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if not isinstance(object_ids, list):
            raise InvalidParams(message='objects parameter is invalid')
        params: Dict[str, Any] = {
            'filter': {
                'ids': object_ids
            }
        }

        if categories is True or isinstance(categories, list):
            params['categories'] = categories

        return self._api.request(
            'cmdb.objects.read',
            params
        )

    def read_by_type(self, object_type: str, categories: Union[List[str], Literal[True]] = None) -> List[Dict]:
        """
        Fetch objects by their object type.

        :param str object_type: Object type constant
        :param categories: (optional) Also fetch category entries;
            add a list of category constants as array of strings or
            ``True`` for all assigned categories
        :type categories: Union[List[str], True, None]
        :return: List of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Any] = {
            'filter': {
                'type': object_type
            }
        }

        if categories is True or isinstance(categories, list):
            params['categories'] = categories

        return self._api.request(
            'cmdb.objects.read',
            params
        )

    def read_archived(self, object_type: str = None, categories: Union[List[str], Literal[True]] = None) -> List[Dict]:
        """
        Fetch archived objects optionally filtered by type

        :param str object_type: (optional) Object type constant
        :param categories: (optional) Also fetch category entries;
            add a list of category constants as array of strings or
            ``True`` for all assigned categories
        :type categories: Union[List[str], True, None]
        :return: List of dicts
        :rtype: list[dict]
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Any] = {
            'filter': {
                'status': 'C__RECORD_STATUS__ARCHIVED'
            }
        }

        if categories is True or isinstance(categories, list):
            params['categories'] = categories

        if object_type is not None:
            params['filter']['type'] = object_type

        return self._api.request(
            'cmdb.objects.read',
            params
        )

    def read_deleted(self, object_type: str = None, categories: Union[List[str], Literal[True]] = None) -> List[Dict]:
        """
        Fetch deleted objects optionally filtered by type

        :param str object_type: (optional) Object type constant
        :param categories: (optional) Also fetch category entries;
            add a list of category constants as array of strings or
            ``True`` for all assigned categories
        :type categories: Union[List[str], True, None]
        :return: List of dicts
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params: Dict[str, Any] = {
            'filter': {
                'status': 'C__RECORD_STATUS__DELETED'
            }
        }

        if categories is True or isinstance(categories, list):
            params['categories'] = categories

        if object_type is not None:
            params['filter']['type'] = object_type

        return self._api.request(
            'cmdb.objects.read',
            params
        )

    def get_id(self, title: str, object_type: str = None) -> int:
        """
        Fetch an object identifier by object title and (optional) type

        :param str title: Object title
        :param str object_type: (optional) type constant
        :return: Object identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        filter_params = {
            'title': title
        }

        if object_type is not None:
            filter_params['type'] = object_type

        result = self.read(filter_params)

        if len(result) == 0:
            raise JSONRPC(message='Object not found')
        elif len(result) == 1:
            if 'id' not in result[0]:
                raise JSONRPC(message='Bad result')
            return result[0]['id']
        else:
            raise JSONRPC(message="Found {} objects".format(len(result)))

    def update(self, objects: List[Dict]) -> None:
        """
        Update one or more existing objects

        :param objects: list of object attributes ('id' and 'title')
        :type objects: list[dict]
        """
        if not isinstance(objects, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(objects) == 0:
            return

        requests = []

        for obj in objects:
            requests.append({
                'method': 'cmdb.object.update',
                'params': obj
            })

        self._api.batch_request(requests)

    def archive(self, object_ids: List[int]) -> None:
        """
        Archive one or more objects

        :param object_ids: List of object identifiers as integers
        :type object_ids: List[int]
        """
        if not isinstance(object_ids, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(object_ids) == 0:
            return

        requests = []

        for obj in object_ids:
            requests.append({
                'method': 'cmdb.object.archive',
                'params': {
                    'object': obj
                }
            })

        self._api.batch_request(requests)

    def delete(self, object_ids: List[int]) -> None:
        """
        Delete one or more objects

        :param object_ids: List of object identifiers as integers
        :type object_ids: List[int]
        """
        if not isinstance(object_ids, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(object_ids) == 0:
            return

        requests = []

        for obj in object_ids:
            requests.append({
                'method': 'cmdb.object.delete',
                'params': {
                    'object': obj
                }
            })

        self._api.batch_request(requests)

    def purge(self, object_ids: List[int]) -> None:
        """
        Purge one or more objects

        :param object_ids: List of object identifiers as integers
        :type object_ids: List[int]
        """
        if not isinstance(object_ids, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(object_ids) == 0:
            return

        requests = []

        for obj in object_ids:
            requests.append({
                'method': 'cmdb.object.purge',
                'params': {
                    'object': obj
                }
            })

        self._api.batch_request(requests)

    def recycle(self, object_ids: List[int]) -> None:
        """
        Restore objects to "normal" status.

        :param object_ids: List of object identifiers as integers
        :type object_ids: List[int]
        """
        if not isinstance(object_ids, list):
            raise InvalidParams(message='objects parameter is invalid')
        if len(object_ids) == 0:
            return

        requests = []

        for object_id in object_ids:
            requests.append({
                'method': 'cmdb.object.recycle',
                'params': {
                    'object': object_id
                }
            })

        self._api.batch_request(requests)
