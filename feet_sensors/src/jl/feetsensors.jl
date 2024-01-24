# AUTO GENERATED FILE - DO NOT EDIT

export feetsensors

"""
    feetsensors(;kwargs...)

A FeetSensors component.

Keyword arguments:
- `id` (String; optional)
- `L0` (Real; required)
- `L1` (Real; required)
- `L2` (Real; required)
- `R0` (Real; required)
- `R1` (Real; required)
- `R2` (Real; required)
- `anomaly_L0` (Bool; required)
- `anomaly_L1` (Bool; required)
- `anomaly_L2` (Bool; required)
- `anomaly_R0` (Bool; required)
- `anomaly_R1` (Bool; required)
- `anomaly_R2` (Bool; required)
"""
function feetsensors(; kwargs...)
        available_props = Symbol[:id, :L0, :L1, :L2, :R0, :R1, :R2, :anomaly_L0, :anomaly_L1, :anomaly_L2, :anomaly_R0, :anomaly_R1, :anomaly_R2]
        wild_props = Symbol[]
        return Component("feetsensors", "FeetSensors", "feet_sensors", available_props, wild_props; kwargs...)
end

