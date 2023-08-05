# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class ChartDefinition(Model):
    """ChartDefinition.

    :param org_chart_definition_id:
    :type org_chart_definition_id: str
    :param name:
    :type name: str
    :param data_source_type:
    :type data_source_type: str
    :param is_public:
    :type is_public: bool
    :param is_promoted:
    :type is_promoted: bool
    :param maximum_depth:
    :type maximum_depth: int
    """

    _attribute_map = {
        'org_chart_definition_id': {'key': 'OrgChartDefinitionId', 'type': 'str'},
        'name': {'key': 'Name', 'type': 'str'},
        'data_source_type': {'key': 'DataSourceType', 'type': 'str'},
        'is_public': {'key': 'IsPublic', 'type': 'bool'},
        'is_promoted': {'key': 'IsPromoted', 'type': 'bool'},
        'maximum_depth': {'key': 'MaximumDepth', 'type': 'int'},
    }

    def __init__(self, **kwargs):
        super(ChartDefinition, self).__init__(**kwargs)
        self.org_chart_definition_id = kwargs.get('org_chart_definition_id', None)
        self.name = kwargs.get('name', None)
        self.data_source_type = kwargs.get('data_source_type', None)
        self.is_public = kwargs.get('is_public', None)
        self.is_promoted = kwargs.get('is_promoted', None)
        self.maximum_depth = kwargs.get('maximum_depth', None)
