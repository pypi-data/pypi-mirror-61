# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class MeRequest(Model):
    """MeRequest.

    :param preference: Preferences for the user
    :type preference: ~energycap.sdk.models.PreferenceRequest
    :param full_name: User's full name
    :type full_name: str
    :param email: User's email address
    :type email: str
    """

    _validation = {
        'full_name': {'max_length': 32},
        'email': {'max_length': 128},
    }

    _attribute_map = {
        'preference': {'key': 'preference', 'type': 'PreferenceRequest'},
        'full_name': {'key': 'fullName', 'type': 'str'},
        'email': {'key': 'email', 'type': 'str'},
    }

    def __init__(self, preference=None, full_name=None, email=None):
        super(MeRequest, self).__init__()
        self.preference = preference
        self.full_name = full_name
        self.email = email
