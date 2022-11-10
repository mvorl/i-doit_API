from typing import Union, Dict, Any, List

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC
from idoitapi.CMDBObjectTypeCategories import CMDBObjectTypeCategories
from idoitapi.CMDBObjects import CMDBObjects
from idoitapi.CMDBCategory import CMDBCategory
from idoitapi.CMDBCategoryInfo import CMDBCategoryInfo


class CMDBObject(Request):
    """
    Requests for API namespace 'cmdb.object'
    """

    def create(self, object_type: Union[int, str], title: str, attributes: Dict = None) -> int:
        """
        Create a new object.

        :param object_type: Object type identifier or constant
        :type object_type: Union[int, str]
        :param str title: Object title
        :param dict attributes: (optional) Dict of additional common attributes:
             * string|int 'category',
             * string|int 'cmdb_status',
             * 0|1 'defaultTemplate',
             * string 'description',
             * string|int 'purpose',
             * int 'status',
             * string 'sysid'
        :return: Object identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'type': object_type,
            'title': title
        }

        if isinstance(attributes, dict):
            params.update(attributes)

        result = self._api.request(
            'cmdb.object.create',
            params
        )

        if 'id' not in result:
            raise JSONRPC(message='Unable to create object')

        return result['id']

    # noinspection PyUnreachableCode
    def create_with_categories(self,
                               object_type: Union[int, str],
                               title: str,
                               categories: Dict,
                               attributes: Dict = None) -> Dict:
        """
        Create a new object with category entries.

        :param object_type: Object type identifier or constant
        :type object_type: Union[int, str]
        :param str title: Object title
        :param dict categories: Also create category entries;
            set category constant (string) as key and
            one (dict of attributes) entry or even several entries (list of dicts) as value
        :param dict attributes: (optional) Dict of additional common attributes:
             * string|int 'category',
             * string|int 'cmdb_status',
             * 0|1 'defaultTemplate',
             * string 'description',
             * string|int 'purpose',
             * int 'status',
             * string 'sysid'
        :return: Result with object identifier ('id') and
            key-value pairs of category constants and array of category entry identifiers as integers
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        if True:

            params: Dict[str, Any] = {
                'type': object_type,
                'title': title
            }

            if isinstance(attributes, dict):
                params.update(attributes)

            if isinstance(categories, dict) and len(categories) != 0:
                params['categories'] = categories

            result = self._api.request(
                'cmdb.object.create',
                params
            )

            if 'id' not in result:
                raise JSONRPC(message='Unable to create object')

        else:
            """
            Note: The proper implementation of this routine was previously disabled
            because of a bug on the server side (with API add-on v1.10.1)
            (cf. `forum discussion <https://community.i-doit.com/topic/3613/>`_)
            """
            object_id = self.create(object_type, title, attributes)

            requests = []

            for category, catattr_array in categories.items():
                for i, catattrs in enumerate(catattr_array):
                    params = {
                        'object': object_id,
                        'category': category,
                        'data': catattrs
                    }
                    if len(catattr_array) > 1:
                        # ToDo: check whether entry ID in a multi-valued category is 0- or 1-based
                        params['entry'] = i
                    requests.append({
                        'method': 'cmdb.category.save',
                        'params': params
                    })

            response = self._api.batch_request(requests)

            result = {
                'id': object_id,
                'success': True,
                'categories': dict(),
            }

            for i, entry in enumerate(response):
                if 'success' not in entry or not entry['success']:
                    self.delete(object_id)
                    message = 'Bad result'
                    if 'message' in entry:
                        message += ': ' + entry['message']
                    raise JSONRPC(message=message)

                params = requests[i]['params']

                category = params['category']
                if 'entry' in params:
                    # For multi-valued categories, value is a list of IDs
                    if category not in result['categories']:
                        result['categories'][category] = []
                    result['categories'][category][params['entry']] = entry['entry']
                else:
                    result['categories'].update({category: entry['entry']})

        return result

    def read(self, object_id: int) -> Dict:
        """
        Read common information about an object.

        :param int object_id: Object identifier
        :return: the object's attributes
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.object.read',
            {
                'id': object_id
            }
        )

    def update(self, object_id: int, attributes: Dict = None) -> None:
        """
        Update existing object

        :param int object_id: Object identifier
        :param dict attributes: (optional) Dict of common attributes
            (only 'title' is supported at the moment)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        params = {
            'id': object_id
        }

        supported_attributes = (
            'title'
        )

        for supported_attribute in supported_attributes:
            if supported_attribute in attributes:
                params[supported_attribute] = attributes[supported_attribute]

        result = self._api.request(
            'cmdb.object.update',
            params
        )

        if 'success' not in result or not result['success']:
            raise JSONRPC(message="Unable to update object {}".format(object_id))

    def archive(self, object_id: int) -> None:
        """
        Archive object

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.archive',
            {
                'id': object_id
            }
        )

    def delete(self, object_id: int) -> None:
        """
        Mark object as deleted (it's still available)

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.delete',
            {
                'id': object_id
            }
        )

    def purge(self, object_id: int) -> None:
        """
        Purge object (delete it irrevocable)

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.purge',
            {
                'id': object_id
            }
        )

    def mark_as_template(self, object_id: int) -> None:
        """
        Convert object to template

        Works only for "normal objects" and "mass change templates"

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.markAsTemplate',
            {
                'id': object_id
            }
        )

    def mark_as_mass_change_template(self, object_id: int) -> None:
        """
        Convert object to mass change template

        Works only for "normal objects" and "templates"

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.markAsMassChangeTemplate',
            {
                'id': object_id
            }
        )

    def recycle(self, object_id: int) -> None:
        """
        Restore object to "normal" status

        Works with archived and deleted objects, templates and mass change templates

        :param int object_id: Object identifier
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        self._api.request(
            'cmdb.object.recycle',
            {
                'object': object_id
            }
        )

    def load(self, object_id: int) -> Dict:
        """
        Load all data about object

        Category information is stored under keys 'catg', 'cats', and 'custom'

        :param int object_id: Object identifier
        :return: data
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        obj = self.read(object_id)

        if len(obj) == 0:
            raise JSONRPC(message='Object not found')

        if 'objecttype' not in obj:
            raise JSONRPC(message="Object {} has no type".format(object_id))

        obj.update(CMDBObjectTypeCategories(self._api).read_by_id(obj['objecttype']))

        cmdb_category = CMDBCategory(self._api)

        category_types = ('catg', 'cats', 'custom')

        blacklisted_category_constants = CMDBCategoryInfo.get_virtual_category_constants()

        for category_type in category_types:
            if category_type not in obj:
                continue

            category_constants = []

            for idx in obj[category_type]:
                if 'const' not in idx:
                    raise JSONRPC(message='Information about categories is broken. Constant is missing.')

                category_constant = idx['const']

                if category_constant in blacklisted_category_constants:
                    continue

                idx['entries'] = []

                category_constants.append(category_constant)

            category_entries = cmdb_category.batch_read([object_id], category_constants)

            for i, c in enumerate(category_constants):
                idx = -1
                entries: List[Dict] = []

                for key, category in enumerate(obj[category_type]):
                    if category.get('const', None) == c:
                        idx = key
                        entries = category_entries[i]
                        break

                obj[category_type][idx]['entries'] = entries

        return obj

    def read_all(self, object_id: int) -> Dict:
        """
        Read all information about object including category entries

        :param int object_id: Object identifier
        :return: information
        :rtype: dict
        """
        objects = CMDBObjects(self._api).read({'ids': [object_id, ]})

        if len(objects) == 0:
            raise JSONRPC(message='Object not found by identifier {}'.format(object_id))
        elif len(objects) != 1:
            raise JSONRPC(message='Found multiple objects by identifier {}'.format(object_id))

        return objects[0]

    def upsert(self, object_type: Union[int, str], title: str, attributes: Dict = None) -> int:
        """
        Create new object or fetch existing one based on its title and type

        :param object_type: Object type identifier or constant
        :type object_type: Union[int, str]
        :param str title: Object title
        :param dict attributes: (optional) Dict of additional common attributes
            ('category', 'purpose', 'cmdb_status', 'description')
        :return: Object identifier
        :rtype: int
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        result = CMDBObjects(self._api).read({
            'title': title,
            'type': object_type
        })

        if len(result) == 0:
            return self.create(object_type, title, attributes)
        elif len(result) == 1:
            if 'id' not in result[0]:
                raise JSONRPC(message='Bad result')
            return result[0]['id']
        else:
            raise JSONRPC(message="Found {} objects".format(len(result)))
