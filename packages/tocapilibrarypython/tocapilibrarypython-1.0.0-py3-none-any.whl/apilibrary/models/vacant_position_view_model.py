# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class VacantPositionViewModel(Model):
    """VacantPositionViewModel.

    All required parameters must be populated in order to send to Azure.

    :param name:
    :type name: str
    :param manager_id: Required.
    :type manager_id: str
    :param position:
    :type position: str
    :param is_temp_position:
    :type is_temp_position: bool
    :param expire_date:
    :type expire_date: datetime
    :param unique_id:
    :type unique_id: str
    :param view_item:
    :type view_item: str
    :param picture_url:
    :type picture_url: str
    :param is_department:
    :type is_department: bool
    :param department_title:
    :type department_title: str
    :param department_text:
    :type department_text: str
    """

    _validation = {
        'manager_id': {'required': True},
    }

    _attribute_map = {
        'name': {'key': 'Name', 'type': 'str'},
        'manager_id': {'key': 'ManagerId', 'type': 'str'},
        'position': {'key': 'Position', 'type': 'str'},
        'is_temp_position': {'key': 'IsTempPosition', 'type': 'bool'},
        'expire_date': {'key': 'ExpireDate', 'type': 'iso-8601'},
        'unique_id': {'key': 'UniqueId', 'type': 'str'},
        'view_item': {'key': 'ViewItem', 'type': 'str'},
        'picture_url': {'key': 'PictureUrl', 'type': 'str'},
        'is_department': {'key': 'IsDepartment', 'type': 'bool'},
        'department_title': {'key': 'DepartmentTitle', 'type': 'str'},
        'department_text': {'key': 'DepartmentText', 'type': 'str'},
    }

    def __init__(self, **kwargs):
        super(VacantPositionViewModel, self).__init__(**kwargs)
        self.name = kwargs.get('name', None)
        self.manager_id = kwargs.get('manager_id', None)
        self.position = kwargs.get('position', None)
        self.is_temp_position = kwargs.get('is_temp_position', None)
        self.expire_date = kwargs.get('expire_date', None)
        self.unique_id = kwargs.get('unique_id', None)
        self.view_item = kwargs.get('view_item', None)
        self.picture_url = kwargs.get('picture_url', None)
        self.is_department = kwargs.get('is_department', None)
        self.department_title = kwargs.get('department_title', None)
        self.department_text = kwargs.get('department_text', None)
