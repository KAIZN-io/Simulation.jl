using Pkg

Pkg.add("AMQPClient")
Pkg.add("JSON")


# get environmetn variables
DEBUG = ENV["DEBUG"]
EXCHANGE_EVENTS = ENV["EXCHANGE_EVENTS"]
SERVICE_SIMULATION_WORKER = ENV["SERVICE_SIMULATION_WORKER"]

# set values
routing_key = "simulation.scheduled"
queue_name = string(SERVICE_SIMULATION_WORKER, "_", routing_key)

# Authentication values
login = "guest"
password = "guest"


using AMQPClient, JSON

auth_params = Dict{String,Any}("MECHANISM"=>"AMQPLAIN", "LOGIN"=>login, "PASSWORD"=>password)
port = AMQPClient.AMQP_DEFAULT_PORT

# open a connection to the server
conn = connection(;virtualhost="/", host="messageBroker", port=port, auth_params=auth_params)
chan = channel(conn, AMQPClient.UNUSED_CHANNEL, true)

# again, declare the queue, just to make sure it exists
success = exchange_declare(chan, EXCHANGE_EVENTS, EXCHANGE_TYPE_TOPIC)
@info success ? "Exchange '$EXCHANGE_EVENTS' declared." : "Couldn't declare exchange '$EXCHANGE_EVENTS'!"

# declare queue
success, message_count, consumer_count = queue_declare(chan, queue_name)
@info success ? "Queue '$queue_name' declared." : "Couldn't declare queue '$queue_name'!"

# bind queue to event exchange
success = queue_bind(chan, queue_name, EXCHANGE_EVENTS, routing_key)
@info success ? "Bound queue '$queue_name' to exchange '$EXCHANGE_EVENTS' using '$routing_key' as routing key." : "Couldn't bind queue '$queue_name' to exchange '$EXCHANGE_EVENTS' with routing key '$routing_key'!"

 # definde the function to be called, when a message arrives
function consumer(msg)
    event = JSON.parse(String(msg.data))
    payload = event["payload"]

    @info string(payload["id"], " - Starting simulation, type: ", payload["type"])

    # here would be the call to start the actual simulation

    @info string(payload["id"], " - Simulation finished.")

    basic_ack(chan, msg.delivery_tag)

    @info string(payload["id"], " - Done.")
end

 # subscribe and register the callback function
success, consumer_tag = basic_consume(chan, queue_name, consumer)
@info success ? "Registered consumer on queue '$queue_name'." : "Couldn't register consumer on queue '$queue_name'!"

@assert success

 # do nothing, to keep the container running. Otherwise, it would just shut down immediately
while true
    sleep(1000)
end

