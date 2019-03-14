using AMQPClient

include("on.jl")
include("emit.jl")
include("simulate.jl")
include("event_creators.jl")


SERVICE_SIMULATION_WORKER = ENV["SERVICE_SIMULATION_WORKER"]

function onSimulationScheduled(ch::AMQPClient.MessageChannel, msg::AMQPClient.Message, event::Dict, payload::Dict)
    @info string(payload["id"], " - Starting simulation, type: ", payload["type"])
    emit(simulationStarted(payload["id"]))

    results = Dict()
    try
        model = Dict(
            "algebraic" => Dict(
                "e" => ["+3*x", "-2*y"],
                "d" => ["+4*y", "-x"],
            ),
            "differential" => Dict(
                "dx" => ["+σ*y", "-σ*x"],
                "dy" => ["+x*ρ" ,"-x*z" ,"- y"],
                "dz" => ["+x*y" ,"- β*z"]
            )
        )

        parameter = Dict(
            "σ" => 10.0, 
            "ρ" => 28.0,
            "β" => 8/3
        )

        initialValues = Dict(
            "x" => 1.01,
            "y" => 1.0,
            "z" => 1.0
        )

        start = 0.0
        stop = 10.0 
        stepSize = 0.2 

        stimuli = [Dict(
            "time" => 5.0,
            "amount" => 5.5,
            "substance" => "x"
        )]



        # here would be the call to start the actual simulation
        results = simulate(model, parameter, initialValues, stimuli, start, stop, stepSize)

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

