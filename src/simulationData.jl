function prepareModel(model::Dict)
    @info model
    algebraic = Array{Dict,1}()
    differential = Array{Dict,1}()
    for (variable, equation) in model["equation"]
        push!(algebraic, Dict(
            "testcd" => variable,
            "orres" => values(equation["component"])
        ))
    end
    for (variable, equation) in model["ODE"]
        push!(differential, Dict(
            "testcd" => variable,
            "orres" => values(equation["component"])
        ))
    end
    return Dict(
        "algebraic" => algebraic,
        "differential" => differential
    )
end

function prepareValues(valueSet::Array)
    ret = Array{Dict,1}()
    for value in valueSet
        push!(ret, Dict(
            "testcd" => value["testcd"],
            "orres" => value["orres"]
        ))
    end
    return ret
end

function prepareParameters(parameterSet::Array)
    return prepareValues(parameterSet)
end

function prepareInitialValues(initialValueSet::Array)
    return prepareValues(initialValueSet)
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

