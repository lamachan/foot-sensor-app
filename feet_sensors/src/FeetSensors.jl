
module FeetSensors
using Dash

const resources_path = realpath(joinpath( @__DIR__, "..", "deps"))
const version = "0.0.1"

include("jl/''_feetsensors.jl")

function __init__()
    DashBase.register_package(
        DashBase.ResourcePkg(
            "feet_sensors",
            resources_path,
            version = version,
            [
                DashBase.Resource(
    relative_package_path = "feet_sensors.min.js",
    external_url = "https://unpkg.com/feet_sensors@0.0.1/feet_sensors/feet_sensors.min.js",
    dynamic = nothing,
    async = nothing,
    type = :js
),
DashBase.Resource(
    relative_package_path = "feet_sensors.min.js.map",
    external_url = "https://unpkg.com/feet_sensors@0.0.1/feet_sensors/feet_sensors.min.js.map",
    dynamic = true,
    async = nothing,
    type = :js
)
            ]
        )

    )
end
end
