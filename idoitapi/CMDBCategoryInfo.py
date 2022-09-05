"""
Requests for API namespace 'cmdb.category_info'
"""

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC
from idoitapi.CMDBObjectTypes import CMDBObjectTypes
from idoitapi.CMDBObjectTypeCategories import CMDBObjectTypeCategories


class CMDBCategoryInfo(Request):

    def read(self, category):
        """
        Fetch information about a category

        :param str category: Category constant
        :return: Result set
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        return self._api.request(
            'cmdb.category_info',
            {
                'category': category
            }
        )

    def batch_read(self, categories):
        """
        Fetches information about one or more categories

        :param categories: List of category constants as strings
        :type categories: list(str)
        :return: Result set
        :rtype: list(dict)
        """
        requests = list()

        for category in categories:
            requests.append({
                'method': 'cmdb.category_info',
                'params': {
                    'category': category
                }
            })

        return self._api.batch_request(requests)

    def read_all(self):
        """
        Try to fetch information about all available categories

        Ignored:
        * Custom categories
        * Categories which are not assigned to any object types

        Notice: This method causes 3 API calls.

        :return: categories' information
        :rtype: dict
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        """
        category_consts = set()
        object_types = CMDBObjectTypes(self._api).read()
        object_type_ids = [object_type['id'] for object_type in object_types]
        object_type_categories_batch = CMDBObjectTypeCategories(self._api).batch_read(object_type_ids)
        cat_types = ('catg', 'cats', 'custom')

        for object_type_categories in object_type_categories_batch:
            for cat_type in cat_types:
                if cat_type not in object_type_categories:
                    continue
                more = [category['const'] for category in object_type_categories[cat_type]]
                category_consts.update(more)

        blacklisted_category_consts = set(self.get_virtual_category_constants())
        clean_category_constants = category_consts - blacklisted_category_consts

        categories = self.batch_read(list(clean_category_constants))

        if len(clean_category_constants) != len(categories):
            raise JSONRPC(message='Unable to restructure result')

        return dict(zip(clean_category_constants, categories))

    @staticmethod
    def get_virtual_category_constants():
        """
        Get list of constants for virtual categories

        "Virtual" means these categories have no attributes at all.

        :return: list of constants
        :rtype: list
        """
        return (
            'C__CATG__CABLING',
            'C__CATG__CABLE_CONNECTION',
            'C__CATG__CLUSTER_SHARED_STORAGE',
            'C__CATG__CLUSTER_VITALITY',
            'C__CATG__CLUSTER_SHARED_VIRTUAL_SWITCH',
            'C__CATG__DATABASE_FOLDER',
            'C__CATG__FLOORPLAN',
            'C__CATG__JDISC_DISCOVERY',
            'C__CATG__LIVESTATUS',
            'C__CATG__MULTIEDIT',
            'C__CATG__NDO',
            'C__CATG__NET_ZONE',
            'C__CATG__NET_ZONE_SCOPES',
            'C__CATG__OBJECT_VITALITY',
            'C__CATG__RACK_VIEW',
            'C__CATG__SANPOOL',
            'C__CATG__STACK_MEMBERSHIP',
            'C__CATG__STACK_PORT_OVERVIEW',
            'C__CATG__STORAGE',
            'C__CATG__VIRTUAL_AUTH',
            'C__CATG__VIRTUAL_RELOCATE_CI',
            'C__CATG__VIRTUAL_SUPERNET',
            'C__CATG__VIRTUAL_TICKETS',
            'C__CATG__VRRP_VIEW',
            'C__CATS__BASIC_AUTH',
            'C__CATS__CHASSIS_CABLING',
            'C__CATS__PDU_OVERVIEW',
        )
