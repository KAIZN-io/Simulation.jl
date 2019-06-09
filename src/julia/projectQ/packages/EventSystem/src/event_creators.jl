using Dates


function simulationStarted(id::Int)
    return Dict(
              "routing_key" => "simulation.started",
              "emitted_at" => Dates.now(),
              "payload" => Dict(
                                "id" => id
                               )
             )
end

function simulationFinished(id::Int, data::Dict)
    return Dict(
              "routing_key" => "simulation.finished",
              "emitted_at" => Dates.now(),
              "payload" => Dict(
                                "id" => id,
                                "extrt" => data["extrt"],
                                "exdose" => data["exdose"],
                                "exstdtc_array" => data["exstdtc_array"],
                                "image_path" => data["image_path"],
                                "pds" => data["pds"]
                               )
             )
end

function simulationFailed(id::Int, error_message::String)
    return Dict(
                  "routing_key" => "simulation.failed",
                  "emitted_at" => Dates.now(),
                  "payload" => Dict(
                                    "id" => id,
                                    "error" => Dict(
                                                    "message" => error_message
                                                   )
                                   )
                 )
end

