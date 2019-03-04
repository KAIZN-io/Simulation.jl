using Pkg
Pkg.add("AMQPClient")

using AMQPClient: Message, MessageChannel

include("on.jl")


SERVICE_SIMULATION_WORKER = ENV["SERVICE_SIMULATION_WORKER"]

function onSimulationScheduled(ch::MessageChannel, msg::Message, event::Dict, payload::Dict)
    @info string(payload["id"], " - Starting simulation, type: ", payload["type"])

    # here would be the call to start the actual simulation

    @info string(payload["id"], " - Simulation finished.")

    basic_ack(ch, msg.delivery_tag)

    @info string(payload["id"], " - Done.")
end

on("simulation.scheduled", onSimulationScheduled, SERVICE_SIMULATION_WORKER)

 # do nothing, to keep the container running. Otherwise, it would just shut down immediately
while true
    sleep(1000)
end

