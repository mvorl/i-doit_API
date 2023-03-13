import os
from typing import Dict, Optional

from idoitapi.Request import Request
from idoitapi.APIException import JSONRPC
from idoitapi.CMDBObject import CMDBObject
from idoitapi.CMDBObjects import CMDBObjects
from idoitapi.CMDBCategory import CMDBCategory
from idoitapi.utils import base64_encode


class File(Request):
    """
    Requests for assigned files
    """

    def add(self, object_id: int, file_path: str, description: Optional[str] = None) -> None:
        """
        Add a new file to a specific object.
        A new file object will be created and assigned to the specific object.

        :param int object_id: Object identifier
        :param str file_path: Path to file
        :param str description: (Optional) description
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        :raises: :py:exc:`OSError` if file not found or unreadable
        """
        file_object_id = CMDBObject(self._api).create(
            'C__OBJTYPE__FILE',
            description if description is not None else ''
        )

        cmdb_category = CMDBCategory(self._api)

        cmdb_category.create(
            file_object_id,
            'C__CATS__FILE_VERSIONS',
            {
                'file_content': base64_encode(file_path),
                'file_physical': os.path.basename(file_path),
                'file_title': description,
                'version_description': description
            }
        )

        cmdb_category.create(
            object_id,
            'C__CATG__FILE',
            {
                'file': file_object_id
            },
        )

    def batch_add(self, object_id: int, files: Dict) -> None:
        """
        Add multiple new files to a specific object.
        New file objects will be created and assigned to the specific object.

        :param int object_id:  Object identifier
        :param dict files: Dict (key: path to file; value: description)
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        :raises: :py:exc:`OSError` if any file not found or unreadable
        """
        objects = []

        for description in files.values():
            objects.append({
                'type': 'C__OBJTYPE__FILE',
                'title': description,
            })

        file_object_ids = CMDBObjects(self._api).create(objects)

        if len(file_object_ids) != len(files):
            raise JSONRPC(
                message='Wanted to create {} file object(s) but got {} object identifiers'.format(
                    len(files), len(file_object_ids)
                )
            )

        requests = []

        counter = 0

        for file_path, description in files.items():
            requests.append({
                'method': 'cmdb.category.create',
                'params': {
                    'objID': file_object_ids[counter],
                    'catsID': 'C__CATS__FILE_VERSIONS',
                    'data': {
                        'file_content': base64_encode(file_path),
                        'file_physical': os.path.basename(file_path),
                        'file_title': description,
                        'version_description': description
                    }
                }
            })

            requests.append({
                'method': 'cmdb.category.create',
                'params': {
                    'objID': object_id,
                    'catgID': 'C__CATG__FILE',
                    'data': {
                        'file': file_object_ids[counter],
                    }
                }
            })

            counter += 1

        self._api.batch_request(requests)
