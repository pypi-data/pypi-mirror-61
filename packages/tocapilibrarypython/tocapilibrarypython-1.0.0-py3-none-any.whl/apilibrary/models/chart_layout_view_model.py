# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChartLayoutViewModel(Model):
    """ChartLayoutViewModel.

    :param id:
    :type id: int
    :param org_chart_definition_id:
    :type org_chart_definition_id: str
    :param unique_id:
    :type unique_id: str
    :param manager_id:
    :type manager_id: str
    :param order:
    :type order: float
    :param sort_flag:
    :type sort_flag: int
    """

    _attribute_map = {
        'id': {'key': 'Id', 'type': 'int'},
        'org_chart_definition_id': {'key': 'OrgChartDefinitionId', 'type': 'str'},
        'unique_id': {'key': 'UniqueId', 'type': 'str'},
        'manager_id': {'key': 'ManagerId', 'type': 'str'},
        'order': {'key': 'Order', 'type': 'float'},
        'sort_flag': {'key': 'SortFlag', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(ChartLayoutViewModel, self).__init__(**kwargs)
        self.id = kwargs.get('id', None)
        self.org_chart_definition_id = kwargs.get('org_chart_definition_id', None)
        self.unique_id = kwargs.get('unique_id', None)
        self.manager_id = kwargs.get('manager_id', None)
        self.order = kwargs.get('order', None)
        self.sort_flag = kwargs.get('sort_flag', None)
