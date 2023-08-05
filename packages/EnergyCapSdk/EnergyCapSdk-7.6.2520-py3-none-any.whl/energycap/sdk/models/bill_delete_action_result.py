# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class BillDeleteActionResult(Model):
    """BillDeleteActionResult.

    :param selected:
    :type selected: int
    :param deleted:
    :type deleted: int
    """

    _attribute_map = {
        'selected': {'key': 'selected', 'type': 'int'},
        'deleted': {'key': 'deleted', 'type': 'int'},
    }

    def __init__(self, selected=None, deleted=None):
        super(BillDeleteActionResult, self).__init__()
        self.selected = selected
        self.deleted = deleted
