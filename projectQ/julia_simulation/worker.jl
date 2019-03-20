using AMQPClient

include("on.jl")
include("emit.jl")
include("simulate.jl")
include("event_creators.jl")
include("simulationData.jl")


SERVICE_SIMULATION_WORKER = ENV["SERVICE_SIMULATION_WORKER"]

function onSimulationScheduled(ch::AMQPClient.MessageChannel, msg::AMQPClient.Message, event::Dict, payload::Dict)
    @info string(payload["id"], " - Starting simulation, type: ", payload["type"])
    emit(simulationStarted(payload["id"]))

    results = Dict()
    try
        model = prepareModel(payload["model"])
        @info model

        parameters = prepareParameters(payload["parameter_set"])
        @info parameters

        initialValues = prepareInitialValues(payload["initial_value_set"])
        @info initialValues

        stimuli = prepareStimuli(payload["stimuli"])
        @info stimuli

        # here would be the call to start the actual simulation
        results = simulate(model, initialValues, parameter, stimuli, payload["start"], payload["stop"], payload["step_size"])

    catch err
        @error string(payload["id"], " - Simulation failed. Error: ", err)

        emit(simulationFailed(payload["id"], string(err)))

        # discard the message form the queue
        basic_reject(ch, msg.delivery_tag)
        return
    end

    @info string(payload["id"], " - Simulation finished.")
    emit(simulationFinished(payload["id"], results))

    # confirm that the message was received and processed
    basic_ack(ch, msg.delivery_tag)

    @info string(payload["id"], " - Done.")
end

on("simulation.scheduled", onSimulationScheduled, SERVICE_SIMULATION_WORKER)

# do nothing, to keep the container running. Otherwise, it would just shut down immediately
while true
    sleep(1000)
end

