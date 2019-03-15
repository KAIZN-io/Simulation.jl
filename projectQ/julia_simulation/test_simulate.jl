using Test

include("simulate.jl")


function testGenerateDeriveFuntion()
    model = Dict(
        "algebraic" => Dict(
            "a" => ["+1*x", "-1*y"],
            "b" => ["+1*y", "-x"],
        ),
        "differential" => Dict(
            "dx" => ["+2σ*y", "-σ*x"],
            "dy" => ["+x*ρ" ,"-x*z" ,"+y"],
            "dz" => ["+2*x*y" ,"-β*z"]
        )
    )

    initialValues = Dict(
        "x" => 1.0,
        "y" => 1.0,
        "z" => 1.0
    )

    parameters = Dict(
        "σ" => 1.0,
        "ρ" => 1.0,
        "β" => 1.0
    )

    derive = generateDeriveFunction(model, initialValues, parameters)

    du = [0.0, 0.0, 0.0]
    u = values(initialValues)
    p = values(parameters)
    t = 0.0
    derive(du, u, p, t)

    @test [1.0, 1.0, 1.0] == du
end

function testSimulate()
    model = Dict(
        "algebraic" => Dict(
            "a" => ["+2*x"],
        ),
        "differential" => Dict(
            "dx" => ["+σ*x", "+a"],
        )
    )

    initialValues = Dict(
        "x" => 1.0,
    )

    parameters = Dict(
        "σ" => 1.0,
    )

    results = simulate(model, initialValues, parameters, [], 0.0, 1.0, 0.1)
    @show results
end

function testVolume()
    model = Dict{String,Dict}(
        "algebraic"=>Dict{String,Array{String}}(
            "R_refdt"=>String["phi*R_ref*r/(2*d)*max(pi_t-pi_c,0)"],
            "r_bdt"=>String["0.2*R_refdt"],
            "R_ref"=>String["r/(1+(1-nu)*(pi_t*r)/(E*2*d))"],
            "V"=>String["4/3*pi*10^(-15)*r^3"],
            "pi_i"=>String["c_i/V*R*T"],
            "V_ref"=>String["4/3*pi*10^(-15)*R_ref^3"],
            "G"=>String["4*pi*r^2"],
            "r_osdt"=>String["-Lp*(pi_t+pi_e-pi_i)"],
            "rdt"=>String["0.2*R_refdt", "-Lp*(pi_t+pi_e-pi_i)"]
        ),
        "differential"=>Dict{String,Array{String}}(
            "dr_b"=>String["r_bdt"],
            "dc_i"=>String["(k_uptake*G-k_consumption*V*(10^15))"],
            "dr_os"=>String["r_osdt"],
            "dr"=>String["rdt"],
            "dR_ref"=>String["R_refdt"],
            "dpi_t"=>String["E*2*d/(1-nu)*(rdt/r^2-R_refdt/(R_ref*r))", "-rdt/r*pi_t"]
        )
    )

    initialValues = Dict{String,String}(
        "r_b"=>"0.496161324363",
        "c_i"=>"0.00000000000638904517734",
        "r_os"=>"1.18773900649",
        "r"=>"1.68390033085",
        "R_ref"=>"1.36108685239",
        "pi_t"=>"200000.0"
    )

    parameters = Dict{String,String}(
        "nu"=>"0.5",
        "modulus_adjustment"=>"(1 - nu ^ 2) ^ (-1)",
        "T"=>"303.15",
        "pi_e"=>"604594.08",
        "phi"=>"0.0001",
        "k_consumption"=>"0.00000000000000025",
        "Lp"=>"0.00000119",
        "d"=>"0.115",
        "E_3D"=>"2580000.0",
        "c_e"=>"240",
        "E"=>"modulus_adjustment * E_3D",
        "k_uptake"=>"0.0000000000000002",
        "pi_c"=>"200000.0",
        "R"=>"8.314",
        "F"=>"96485"
    )

    results = simulate(model, initialValues, parameters, [], 0.0, 1.0, 1.0)
    @show results
end

function exampleVolume()
    tspan = (0.0,1.0)

    initialValues = [
        0.496161324363,            # r_b
        0.00000000000638904517734, # c_i
        1.18773900649,             # r_os
        1.68390033085,             # r
        1.36108685239,             # R_ref
        200000.0                   # pi_t
    ]

    parameters = Float64[
        0.5,                 # nu
        303.15,              # T
        604594.08,           # pi_e
        0.0001,              # phi
        0.00000000000000025, # k_consumption
        0.00000119,          # Lp
        0.115,               # d
        2580000.0,           # E_3D
        240,                 # c_e
        0.0000000000000002,  # k_uptake
        200000.0,            # pi_c
        8.314,               # R
        96485                # F
    ]

    function diff(du, values, parameters, time)
        # initial values
        r_b, c_i, r_os, r, R_ref, pi_t = values

        # Parameters
        nu, T, pi_e, phi, k_consumption, Lp, d, E_3D, c_e, k_uptake, pi_c, R, F = parameters
        modulus_adjustment = (1 - nu ^ 2) ^ (-1)
        E = modulus_adjustment * E_3D

        # algebraic equations
        R_refdt = phi*R_ref*r/(2*d)*max(pi_t-pi_c,0)
        r_bdt   = 0.2*R_refdt
        R_ref   = r/(1+(1-nu)*(pi_t*r)/(E*2*d))
        V       = 4/3*pi*10^(-15)*r^3
        pi_i    = c_i/V*R*T
        V_ref   = 4/3*pi*10^(-15)*R_ref^3
        G       = 4*pi*r^2
        r_osdt  = -Lp*(pi_t+pi_e-pi_i)
        rdt     = 0.2*R_refdt -Lp*(pi_t+pi_e-pi_i)

        # calculate du
        du[1] = dr_b   = r_bdt
        du[2] = dc_i   = (k_uptake*G-k_consumption*V*(10^15))
        du[3] = dr_os  = r_osdt
        du[4] = dr     = rdt
        du[5] = dR_ref = R_refdt
        du[6] = dpi_t  = E*2*d/(1-nu)*(rdt/r^2-R_refdt/(R_ref*r)) -rdt/r*pi_t
    end

    function noise(du,u,p,t)
      du[1] = 0
      du[2] = 0
      du[3] = 0
      du[4] = 0
      du[5] = 0
      du[6] = 0
    end

    prob = SDEProblem(diff,noise,initialValues,tspan,parameters,seed=1234)

    res = diffeq_fd(prob.p,sol->sol[1:6,:],66,prob,SOSRI(),saveat=0.1)

    @show res
end

