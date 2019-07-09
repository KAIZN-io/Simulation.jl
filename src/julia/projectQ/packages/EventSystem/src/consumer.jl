using AMQPClient


# get environmetn variables
EXCHANGE_EVENTS = get( ENV, "EXCHANGE_EVENTS", "default-exchange" )

# Authentication values
# TODO: Make this dynamic and not plain text
login = "guest"
password = "guest"

# connection parameters
auth_params = Dict{String,Any}("MECHANISM"=>"AMQPLAIN", "LOGIN"=>login, "PASSWORD"=>password)
port = AMQPClient.AMQP_DEFAULT_PORT

function consume(event_name::String, callback::Function, queue::String)
    # open a connection to the server
    conn = connection(;virtualhost="/", host="messageBroker", port=port, auth_params=auth_params)
    ch = channel(conn, AMQPClient.UNUSED_CHANNEL, true)

    # declare the events exchange
    success = exchange_declare(ch, EXCHANGE_EVENTS, EXCHANGE_TYPE_TOPIC)
    @info success ? "Exchange '$EXCHANGE_EVENTS' declared." : "Couldn't declare exchange '$EXCHANGE_EVENTS'!"

    # declare queue
    success, message_count, consumer_count = queue_declare(ch, queue)
    @info success ? "Named queue '$queue' declared. Message count: $message_count" : "Couldn't declare queue '$queue'!"

    # bind queue
    success = queue_bind(ch, queue, EXCHANGE_EVENTS, event_name)
    @info success ? "Bound queue '$queue' to exchange '$EXCHANGE_EVENTS' using '$event_name' as routing key." : "Couldn't bind queue '$queue' to exchange '$EXCHANGE_EVENTS' with routing key '$event_name'!"

    # subscribe and register the callback function
    success, consumer_tag = basic_consume(ch, queue, (msg) -> callback(ch, msg))
    @info success ? "Registered consumer '$callback' on queue '$queue'" : "Couldn't register consumer '$callback' on queue '$queue'!"

    @assert success

end

