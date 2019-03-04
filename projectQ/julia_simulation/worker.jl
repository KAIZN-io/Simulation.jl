using Pkg
Pkg.add("AMQPClient")

using AMQPClient: Message, MessageChannel
using Dates

include("on.jl")
include("emit.jl")
include("simulate.jl")


SERVICE_SIMULATION_WORKER = ENV["SERVICE_SIMULATION_WORKER"]

function onSimulationScheduled(ch::MessageChannel, msg::Message, event::Dict, payload::Dict)
    @info string(payload["id"], " - Starting simulation, type: ", payload["type"])
    emit(
         Dict(
              "routing_key" => "simulation.started",
              "emitted_at" => Dates.now(),
              "payload" => Dict(
                                "id" => payload["id"]
                               )
             )
        )

    results = Dict()
    try
        # here would be the call to start the actual simulation
        results = simulate(payload)
    catch err
        @error string(payload["id"], " - Simulation failed. Error: ", err)

        emit(
             Dict(
                  "routing_key" => "simulation.failed",
                  "emitted_at" => Dates.now(),
                  "payload" => Dict(
                                    "id" => payload["id"],
                                    "error" => Dict(
                                                    "message" => err
                                                   )
                                   )
                 )
            )

        # discard the message form the queue
        basic_reject(ch, msg.delivery_tag)
        return
    end

    @info string(payload["id"], " - Simulation finished.")
    emit(
         Dict(
              "routing_key" => "simulation.finished",
              "emitted_at" => Dates.now(),
              "payload" => Dict(
                                "id" => payload["id"],
                                "extrt" => results["extrt"],
                                "exdose" => results["exdose"],
                                "exstdtc_array" => results["exstdtc_array"],
                                "image_path" => results["image_path"],
                                "pds" => results["pds"]
                               )
             )
        )

    # confirm that the message was received and processed
    basic_ack(ch, msg.delivery_tag)

    @info string(payload["id"], " - Done.")
end

on("simulation.scheduled", onSimulationScheduled, SERVICE_SIMULATION_WORKER)

# do nothing, to keep the container running. Otherwise, it would just shut down immediately
while true
    sleep(1000)
end

