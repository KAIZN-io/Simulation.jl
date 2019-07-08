module Simulator

using AMQPClient
using EventSystem: on, emit, simulationStarted, simulationFailed, simulationFinished
using Simulation: simulate


# TODO: rename env var to service / package naming convention
SERVICE_SIMULATION_WORKER = get( ENV, "SERVICE_SIMULATION_WORKER", "simulator" )

function prepareModel(model::Dict)
    @info model
    algebraic = Dict()
    differential = Dict()
    for (variable, equation) in model["equation"]
        algebraic[variable] = values(equation["component"])
    end
    for (variable, equation) in model["ODE"]
        differential[variable] = values(equation["component"])
    end
    return Dict(
        "algebraic" => algebraic,
        "differential" => differential
    )
end

function prepareParameters(parameterSet::Array)
    ret = Dict()
    for parameter in parameterSet
        ret[parameter["testcd"]] = parameter["orres"]
    end
    return ret
end

function prepareInitialValues(InitialValueSet::Array)
    ret = Dict()
    for initialValue in InitialValueSet
        ret[initialValue["testcd"]] = initialValue["orres"]
    end
    return ret
end

function prepareStimuli(Stimuli::Array)
    ret = []
    for stimulus in Stimuli
        # ret[initialValue["testcd"]] = initialValue["orres"]
        for target in stimulus["targets"]
            for timePoint in stimulus["timings"]
                push!(ret, Dict(
                    "time" => timePoint,
                    "amount" => stimulus["amount"],
                    "substance" => target
                ))
            end
        end
    end
    return ret
end

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

function run()
    on("simulation.scheduled", onSimulationScheduled, SERVICE_SIMULATION_WORKER)

    # do nothing, to keep the container running. Otherwise, it would just shut down immediately
    while true
        sleep(1000)
    end
end

end # module Simulator

