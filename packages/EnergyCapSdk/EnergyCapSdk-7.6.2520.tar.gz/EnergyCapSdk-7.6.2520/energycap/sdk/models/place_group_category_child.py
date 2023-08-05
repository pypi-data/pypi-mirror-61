# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class PlaceGroupCategoryChild(Model):
    """PlaceGroupCategoryChild.

    :param place_group_category_id:
    :type place_group_category_id: int
    :param place_group_category_code:
    :type place_group_category_code: str
    :param place_group_category_info:
    :type place_group_category_info: str
    """

    _attribute_map = {
        'place_group_category_id': {'key': 'placeGroupCategoryId', 'type': 'int'},
        'place_group_category_code': {'key': 'placeGroupCategoryCode', 'type': 'str'},
        'place_group_category_info': {'key': 'placeGroupCategoryInfo', 'type': 'str'},
    }

    def __init__(self, place_group_category_id=None, place_group_category_code=None, place_group_category_info=None):
        super(PlaceGroupCategoryChild, self).__init__()
        self.place_group_category_id = place_group_category_id
        self.place_group_category_code = place_group_category_code
        self.place_group_category_info = place_group_category_info
