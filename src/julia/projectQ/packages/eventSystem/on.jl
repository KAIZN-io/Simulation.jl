using JSON
using AMQPClient: Message, MessageChannel, basic_reject

include("consumer.jl")


function on(event_name::String, callback::Function, durable_for_service_name::String)

    function callback_wrapper(ch::MessageChannel, msg::Message)
        event = Dict()
        payload = Dict()
        try
            event = JSON.parse(String(msg.data))
            payload = event["payload"]
        catch err
            @error err
            basic_reject(ch, msg.delivery_tag)
            return
        end

        callback(ch, msg, event, payload)
    end

    queue = string(durable_for_service_name, "_", event_name)

    consume(event_name, callback_wrapper, queue)
end

