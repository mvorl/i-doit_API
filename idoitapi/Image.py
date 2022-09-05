"""
Requests for image galleries
"""

from idoitapi.Request import Request
from idoitapi.CMDBCategory import CMDBCategory
from idoitapi.utils import base64_encode


class Image(Request):

    def add(self, object_id, file_path, caption=None):
        """
        Add a new file to the image gallery.

        :param int object_id: Object identifier
        :param str file_path: Path to image file
        :param str caption: (Optional) caption
        :return: self
        :rtype: object
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

        return self

    def batch_add(self, object_id, images):
        """
        Add new files to the image gallery.

        :param int object_id: Object identifier
        :param images: Dict (key: path to image file; value: caption)
        :type images: dict(str, str)
        :return: self
        :rtype: object
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

        return self
