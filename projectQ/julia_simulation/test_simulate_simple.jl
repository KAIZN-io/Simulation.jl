using Test

include("simulate.jl")

start = 0.0
stop = 1.0
step_size = 0.1
noise_level = 0.0
seed = 1337

function dynamicSimpleSimulation()
    initialValues = Dict{String,String}(
        "a"=>"1.0",
        "b"=>"2.0"
    )

    parameters = Dict{String,String}(
        "roh"=>"0.5",
        "phi"=>"0.25"
    )

    model = Dict{String,Dict}(
        "algebraic"=>Dict{String,Array{String}}(
            "a_roh"=>String["a + roh"],
            "b_phi"=>String["b + phi"]
        ),
        "differential"=>Dict{String,Array{String}}(
            "da"=>String["a / a_roh"],
            "db"=>String["b / b_phi"]
        )
    )

    res = simulate(model, initialValues, parameters, [], start, stop, step_size, noise_level, seed)

    return res
end

function staticSimpleSimulation()
    initialValues = [
        1.0, # a
        2.0  # b
    ]

    parameters = [
        0.5, # roh
        0.25 # phi
    ]

    function diff(du, values, parameters, time)
        # initial values
        a, b = values

        # Parameters
        roh, phi = parameters

        # algebraic equations
        a_roh = a + roh
        b_phi = b + phi

        # calculate du
        du[1] = da = a / a_roh
        du[2] = db = b / b_phi
    end

    # not using any noise
    function noise(du,u,p,t)
      du[1] = noise_level
      du[2] = noise_level
    end

    prob = SDEProblem(diff,noise,initialValues,(start,stop),parameters,seed=seed)

    res = diffeq_fd(prob.p,sol->sol[1:2,:],22,prob,SOSRI(),saveat=step_size)

    return Dict(
        "a" => res[1, :],
        "b" => res[2, :]
    )
end

function testSimpleSimulation()
    dyn_res = dynamicSimpleSimulation()
    @show dyn_res

    sta_res = staticSimpleSimulation()
    @show sta_res

    @test dyn_res == sta_res
end

