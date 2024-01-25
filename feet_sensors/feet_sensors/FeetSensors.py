# AUTO GENERATED FILE - DO NOT EDIT

from dash.development.base_component import Component, _explicitize_args


class FeetSensors(Component):
    """A FeetSensors component.
Custom component of 2 feet with 3 sensors on each foot.

Keyword arguments:

- id (string; optional):
    Component ID.

- L0 (number; required):
    Value of the L0 sensor.

- L1 (number; required):
    Value of the L0 sensor.

- L2 (number; required):
    Value of the L0 sensor.

- R0 (number; required):
    Value of the L0 sensor.

- R1 (number; required):
    Value of the L0 sensor.

- R2 (number; required):
    Value of the L0 sensor.

- anomaly_L0 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor.

- anomaly_L1 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor.

- anomaly_L2 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor.

- anomaly_R0 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor.

- anomaly_R1 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor.

- anomaly_R2 (boolean; required):
    Boolean value informing if there is an anomaly on the L0 sensor."""
    _children_props = []
    _base_nodes = ['children']
    _namespace = 'feet_sensors'
    _type = 'FeetSensors'
    @_explicitize_args
    def __init__(self, id=Component.UNDEFINED, L0=Component.REQUIRED, L1=Component.REQUIRED, L2=Component.REQUIRED, R0=Component.REQUIRED, R1=Component.REQUIRED, R2=Component.REQUIRED, anomaly_L0=Component.REQUIRED, anomaly_L1=Component.REQUIRED, anomaly_L2=Component.REQUIRED, anomaly_R0=Component.REQUIRED, anomaly_R1=Component.REQUIRED, anomaly_R2=Component.REQUIRED, **kwargs):
        self._prop_names = ['id', 'L0', 'L1', 'L2', 'R0', 'R1', 'R2', 'anomaly_L0', 'anomaly_L1', 'anomaly_L2', 'anomaly_R0', 'anomaly_R1', 'anomaly_R2']
        self._valid_wildcard_attributes =            []
        self.available_properties = ['id', 'L0', 'L1', 'L2', 'R0', 'R1', 'R2', 'anomaly_L0', 'anomaly_L1', 'anomaly_L2', 'anomaly_R0', 'anomaly_R1', 'anomaly_R2']
        self.available_wildcard_properties =            []
        _explicit_args = kwargs.pop('_explicit_args')
        _locals = locals()
        _locals.update(kwargs)  # For wildcard attrs and excess named props
        args = {k: _locals[k] for k in _explicit_args}

        for k in ['L0', 'L1', 'L2', 'R0', 'R1', 'R2', 'anomaly_L0', 'anomaly_L1', 'anomaly_L2', 'anomaly_R0', 'anomaly_R1', 'anomaly_R2']:
            if k not in args:
                raise TypeError(
                    'Required argument `' + k + '` was not specified.')

        super(FeetSensors, self).__init__(**args)
