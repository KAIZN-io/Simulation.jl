module EventSystem

include("on.jl")
include("emit.jl")

export on, emit, simulationStarted, simulationFailed, simulationFinished

end

