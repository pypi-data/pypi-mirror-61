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

    def __init__(self, *, manager_id: str, name: str=None, position: str=None, is_temp_position: bool=None, expire_date=None, unique_id: str=None, view_item: str=None, picture_url: str=None, is_department: bool=None, department_title: str=None, department_text: str=None, **kwargs) -> None:
        super(VacantPositionViewModel, self).__init__(**kwargs)
        self.name = name
        self.manager_id = manager_id
        self.position = position
        self.is_temp_position = is_temp_position
        self.expire_date = expire_date
        self.unique_id = unique_id
        self.view_item = view_item
        self.picture_url = picture_url
        self.is_department = is_department
        self.department_title = department_title
        self.department_text = department_text
