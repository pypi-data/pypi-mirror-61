# ----------------------------------------------------------------------------------------------------
# IBM Confidential
# OCO Source Materials
# 5900-A3Q, 5737-J33
# Copyright IBM Corp. 2018
# The source code for this program is not published or other-wise divested of its trade 
# secrets, irrespective of what has been deposited with the U.S.Copyright Office.
# ----------------------------------------------------------------------------------------------------

from ibm_ai_openscale.utils import *


class BusinessMetric:
    """
    Used during application registration, describes metrics passed to business application.

    :param metric_name: name of the metric
    :type metric_name: str
    :param field_name: name of the field which metric is calculated on
    :type field_name: str
    :param aggregation: type of calculation method supported by applications. One of: ['sum', 'min', 'max', 'avg']
    :type aggregation: str
    :param time_unit:  one of: [ 'day', 'week', 'month' ], default: 'day'
    :type time_unit: str
    :param time_count: default: 1
    :type time_count: int
    :param description: description of the metric (optional)
    :type description: str
    :param lower_limit: lower control limit default value (optional)
    :type lower_limit: float
    :param upper_limit: upper control limit default value (optional)
    :type upper_limit: float
    :param required: is this metric obligatory?, default value: True
    :type required: bool
    """

    def __init__(self, metric_name, field_name, aggregation , time_unit='day', time_count=1, description=None, lower_limit=None, upper_limit=None, required=True, ):
        validate_type(metric_name, 'metric_name', str, True)
        validate_type(field_name, 'field_name', str, True)
        validate_type(aggregation, 'aggregation', str, True)
        validate_type(time_unit, 'time_unit', str, True)
        validate_type(time_count, 'time_count', int, True)
        validate_type(description, 'description', str, False)
        validate_type(required, 'required', bool, False)

        try:
            validate_type(lower_limit, 'lower_limit', float, False)
        except:
            validate_type(lower_limit, 'lower_limit', int, False)
        try:
            validate_type(upper_limit, 'lower_limit', float, False)
        except:
            validate_type(upper_limit, 'lower_limit', int, False)

        if aggregation not in ['sum', 'min', 'max', 'avg']:
            raise IncorrectValue(value_name='data_format', reason='Unsupported value.')

        if time_unit not in ['day', 'week', 'month']:
            raise IncorrectValue(value_name='data_format', reason='Unsupported value.')

        self.metric_name = metric_name
        self.description = description
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.required = required
        self.thresholds = []
        self.calculation_metadata = {'field_name': field_name,
                                     'aggregation': aggregation,
                                     'time_frame': {
                                         'count': time_count,
                                         'unit': time_unit
                                     }}

        if self.lower_limit is not None:
            self.thresholds.append({"type": "lower_limit", "default": self.lower_limit})

        if self.upper_limit is not None:
            self.thresholds.append({"type": "upper_limit", "default": self.upper_limit})

    def _to_json(self):
        json_object = {
            'name': self.metric_name,
            'required': self.required,
            'calculation_metadata': self.calculation_metadata
        }

        if self.description is not None:
            json_object['description'] = self.description

        if len(self.thresholds) > 0:
            json_object['thresholds'] = self.thresholds

        return json_object
