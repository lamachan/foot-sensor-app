# AUTO GENERATED FILE - DO NOT EDIT

export ''_feetsensors

"""
    ''_feetsensors(;kwargs...)

A FeetSensors component.
Custom component of 2 feet with 3 sensors on each foot.
Keyword arguments:
- `id` (String; optional): Component ID.
- `L0` (Real; required): Value of the L0 sensor.
- `L1` (Real; required): Value of the L0 sensor.
- `L2` (Real; required): Value of the L0 sensor.
- `R0` (Real; required): Value of the L0 sensor.
- `R1` (Real; required): Value of the L0 sensor.
- `R2` (Real; required): Value of the L0 sensor.
- `anomaly_L0` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
- `anomaly_L1` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
- `anomaly_L2` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
- `anomaly_R0` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
- `anomaly_R1` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
- `anomaly_R2` (Bool; required): Boolean value informing if there is an anomaly on the L0 sensor.
"""
function ''_feetsensors(; kwargs...)
        available_props = Symbol[:id, :L0, :L1, :L2, :R0, :R1, :R2, :anomaly_L0, :anomaly_L1, :anomaly_L2, :anomaly_R0, :anomaly_R1, :anomaly_R2]
        wild_props = Symbol[]
        return Component("''_feetsensors", "FeetSensors", "feet_sensors", available_props, wild_props; kwargs...)
end

