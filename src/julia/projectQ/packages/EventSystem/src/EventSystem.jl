module EventSystem

include("event_creators.jl")
include("on.jl")
include("emit.jl")

export on, emit, simulationStarted, simulationFailed, simulationFinished

end

