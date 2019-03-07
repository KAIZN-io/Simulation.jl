using Pkg
Pkg.add("DiffEqFlux")
Pkg.add("DifferentialEquations")

using DiffEqFlux, DifferentialEquations


function generateNoiseFunction(noise=0.01)
    return noiseFunction(du,u,p,t) = @.(du = noise)
end

"""
Generates a dynamic derive function for an SDE problem

This function will use its arguments to create a dynamic derive function that
can be used in a SDE problem.

Dynamic meaning it can work with any number of differential equations. It does
so by not having any hard coded deriviatives, but works on the given `model`,
`initialValues` and `parameters` using eval.

It expets to find the differential equations inside the `model` dict. It will
evaluate all the given parameters in the beginning. This way these never
changing parameters can be accessed in the inner `derive` function - even when
the returned `derive` function is called inside a SDE solver.

The arguments need to have the shape as dclared for the `simulate` function.
"""
function generateDeriveFunction(model::Dict, initialValues::Dict, parameters::Dict)
    # List of initial value and parameter variables. The keys of the dicts are
    # variable names. We declare them here, so they can be used in the `derive`
    # function below.
    initialValueKeys = collect(keys(initialValues))
    parameterKeys = collect(keys(parameters))

    # Evaluate all parameters so we can work with them later in the `derive`
    # function.
    for (parameter, value) in parameters
        eval(Meta.parse(string(parameter, "=", value)))
    end

    """
    The dynamic derive function

    This derive function can work with a variable amount of differential
    equations.
    """
    function derive(du, valueList, parameterList, t)
        # Evaluate the current values (u) to be used in declaring the
        # derivatives. We enumerate the values, so that we have an numeric
        # index for each value. With this index, we can retrieve the variable
        # name from the initial values (using the `initialValueKeys` list).
        for (index, value) in enumerate(valueList)
            eval(Meta.parse(string(initialValueKeys[index], "=", value)))
        end

        # With the current values (u) evaluated, we can evaluate the algebraic
        # equations from the `model`. We need to do this tep here, as the
        # algebraic equations can be dependent on the (initial) values (u).
        for (var, terms) in model["algebraic"]
            eval(Meta.parse(string(var, "=", join(terms))))
        end

        # Calculate derivatives
        # Here we enumerate the `valueList` again to have a numeric index. This
        # index is used to retrieve the name of the variable from the
        # (initial) values (using the `initialValueKeys` list). With the name
        # of that variable, we can look up the corresponding differential
        # equation from the `model` by prepending a 'd' to the variable name.
        for (index, value) in enumerate(valueList)
            # Get the name of the variable
            var = initialValueKeys[index]
            # look up its corresponding differential equation
            diffeq = model["differential"][string("d", var)]
            # evaluate the differential equation
            du[index] = eval(Meta.parse(join(diffeq)))
        end
    end

    return derive
end

"""
Generate a SDE problem dynamic in the amount of differential equations

This function generates a SDE problem where the amount of differential
equations can be dynamic. This amount is defined by the differential equations
found in the `model` parameter.
It does that by using a special derive function that has no static code but
uses eval on the given `model`, `initialValues` and `parameters`.

The arguments need to be in the same shape as defined for the `simulate`
function.
"""
function generateSdeProblem(model::Dict, initialValues::Dict, parameters::Dict, start::Float64, stop::Float64, seed = 1234)
    # Get the derive function
    derive = generateDeriveFunction(model, initialValues, parameters)

    # Get the noise function
    noise = generateNoiseFunction()

    # Set the time span
    timeSpan = (start, stop)

    # declare the SDE problem
    return SDEProblem(derive, noise, values(initialValues), timeSpan, values(parameters), seed = seed)
end

"""
Generate a solving function for a given SDE problem

Given an SDE problem, the desired step size and a list of stimuli, this
function sets some values, creates and finally returns a function that can be
used to solve the given SDE problem.

The values are set inside this function, so that the inner `solve` function can
access and work with these values.

The stimuli array and the initial values need to be in the same shape as for
the `simulate` function.
"""
function generateSolveFunction(sdeProblem, initialValues::Dict, stimuli::Array, stepSize::Float64, solver=SOSRI())
    # Retrieve time values from the given SDE problem
    start = sdeProblem.tspan[1]
    stop = sdeProblem.tspan[2]

    # Retrieve the parameters from the SDE problem
    parameters = sdeProblem.p

    # Create a list with all stimuli time points at which we want to interrupt
    # the solving to let our stimuli take effect.
    stimuliTimePoints = map((stimulus)->stimulus["time"],stimuli)
    @info string("Stimuli time points: ", stimuliTimePoints)

    # Create a list of time points that we want to retrieve results for. This
    # list will include time points as floating point numbers. From `start` to
    # `stop` we will have an entry every `stepSize`. Additionally, we add the
    # points, where stimuli need to be actiavted.
    frames = sort(unique(append!(collect(start:stepSize:stop), stimuliTimePoints)))
    @info string("Frames: ", frames)

    ### Define callbacks for setting stimuli###

    # Callback to check whether a stimuli needs to be triggered
    function isStimulusActive(u,t,integrator)
        return t in stimuliTimePoints
    end

    # Callback to activate a stimuli, adding its value to a value in the SDE
    # problem.
    initialValueKeys = collect(keys(initialValues))
    function activateStimulus!(integrator)
        # Iterate over all stimuli to find active ones
        for stimulus in stimuli
            # If the time for the stimulus to be active has come
            if stimulus["time"] == integrator.t
                # Find the index of the stimulus substance in the (initial) values
                index = findfirst(val -> val == stimulus["substance"], initialValueKeys)
                # Add the stimulus amount to its corresponding value
                integrator.u[index] += stimulus["amount"]
            end
        end
    end

    # This discrete callback will use the `isStimuliActive` function to check and
    # calls the `activateStimulus!` function when `isStimuliActive` returns
    # true, meaning when a stimulus needs to take effect.
    stimuliCallback = DiscreteCallback(isStimulusActive, activateStimulus!)


    # Getting sunstance and frame count so that we get results for all substances back
    substanceCount = length(initialValueKeys)
    frameCount = length(frames)
    resultLength = (frameCount + 1) * substanceCount # +1 for the initial value column in the result matrix
    @info string("Calculated result length: ", resultLength)

    function solve()
        diffeq_fd(
            parameters,
            sol->sol[1:substanceCount,:],
            resultLength,
            sdeProblem,
            solver,
            saveat = frames,
            callback = stimuliCallback,
            tstops = stimuliTimePoints
        )
    end

    return solve
end

"""
Run a simulation with a dynamic amount of differential equations

This function solves a SDE problem given a dynamic set of differential
equations, initial values and parameters.

The arguments are expected to look like this:

```
model = Dict(
    "algebraic" => Dict(
        "e" => ["+3*x", "-2*x"],
        ...
    ),
    "differential" => Dict(
        "dx" => ["+σ*x", "-σ*x"],
        ...
    )
)

initialValues = Dict(
    "x" => 1.01,
    ...
)

parameters = Dict(
    "σ" => 10.0,
    ...
)

stimuli = [
    Dict(
        "time" => 5.0,
        "amount" => 5.5,
        "substance" => "x"
    ),
    ...
]
```
"""
function simulate(model::Dict, initialValues::Dict, parameters::Dict, stimuli::Array, start::Float64, stop::Float64, stepSize::Float64)
    # generate the SDE problem from the given arguments
    sdeProblem = generateSdeProblem(model, initialValues, parameters, start, stop)

    # generate the solving function for the SDE problem
    solve = generateSolveFunction(sdeProblem, initialValues, stimuli, stepSize)

    # solve the sde problem
    res = solve()
    @info string("Actual result length:.... ", length(res))
    @info "Results:"
    @show res

    return res
end

