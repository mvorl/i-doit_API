from typing import Dict

from idoitapi.Request import Request
from idoitapi.CMDBCategory import CMDBCategory
from idoitapi.utils import base64_encode


class Image(Request):
    """
    Requests for image galleries
    """

    def add(self, object_id: int, file_path: str, caption: str = None) -> None:
        """
        Add a new file to the image gallery.

        :param int object_id: Object identifier
        :param str file_path: Path to image file
        :param str caption: (Optional) caption
        :raises: :py:exc:`~idoitapi.APIException.APIException` on error
        :raises: :py:exc:`OSError` if file not found or unreadable
        """
        CMDBCategory(self._api).create(
            object_id,
            'C__CATG__IMAGES',
            {
                'name': caption,
                'content': base64_encode(file_path)
            }
        )

    def batch_add(self, object_id: int, images: Dict) -> None:
        """
        Add new files to the image gallery.

        :param int object_id: Object identifier
        :param dict images: Dict (key: path to image file; value: caption)
        :raises: :py:exc:`OSError` if any file not found or unreadable
        """
        object_ids = [object_id, ]
        category_const = 'C__CATG__IMAGES'
        attributes = []

        for file_path, caption in images.items():
            attributes.append({
                'name': caption,
                'content': base64_encode(file_path)
            })

        CMDBCategory(self._api).batch_create(object_ids, category_const, attributes)
