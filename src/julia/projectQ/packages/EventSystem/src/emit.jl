using JSON, AMQPClient


# get environmetn variables
EXCHANGE_EVENTS = get( ENV, "EXCHANGE_EVENTS", "default-exchange" )

# Authentication values
login = "guest"
password = "guest"

# connection parameters
auth_params = Dict{String,Any}("MECHANISM"=>"AMQPLAIN", "LOGIN"=>login, "PASSWORD"=>password)
port = AMQPClient.AMQP_DEFAULT_PORT

function emit(event::Dict)

    # open a connection to the server
    conn = connection(;virtualhost="/", host="messageBroker", port=port, auth_params=auth_params)
    ch = channel(conn, AMQPClient.UNUSED_CHANNEL, true)

    # declare the events exchange
    success = exchange_declare(ch, EXCHANGE_EVENTS, EXCHANGE_TYPE_TOPIC)
    @assert success

    # publish the message
    msg = Message(Vector{UInt8}(JSON.json(event)))
    basic_publish(ch, msg;
        exchange=EXCHANGE_EVENTS,
        routing_key=event["routing_key"],
    )

    # close the connection
    close(conn)
end

