# dummy implementation of the simulation function
function simulate(data::Dict)
    sleep(6)
    return Dict(
                "extrt" => "No actual value",
                "exdose" => -1,
                "exstdtc_array" => [],
                "image_path" => "non_existing_image.png",
                "pds" => []
               )
end

