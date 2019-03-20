using Test

include("simulate.jl")

start = 0.0
stop = 1.0
step_size = 0.1
noise_level = 0.0
seed = 1337

function dynamicVolumeSimulation()
    model = Dict(
        "algebraic"=>[
            Dict("testcd"=>"R_refdt", "orres"=>["phi*R_ref*r/(2*d)*max(pi_t-pi_c,0)"]),
            Dict("testcd"=>"r_bdt",   "orres"=>["0.2*R_refdt"]),
            Dict("testcd"=>"R_ref",   "orres"=>["r/(1+(1-nu)*(pi_t*r)/(E*2*d))"]),
            Dict("testcd"=>"V",       "orres"=>["4/3*pi*10^(-15)*r^3"]),
            Dict("testcd"=>"pi_i",    "orres"=>["c_i/V*R*T"]),
            Dict("testcd"=>"V_ref",   "orres"=>["4/3*pi*10^(-15)*R_ref^3"]),
            Dict("testcd"=>"G",       "orres"=>["4*pi*r^2"]),
            Dict("testcd"=>"r_osdt",  "orres"=>["-Lp*(pi_t+pi_e-pi_i)"]),
            Dict("testcd"=>"rdt",     "orres"=>["0.2*R_refdt", "-Lp*(pi_t+pi_e-pi_i)"])
        ],
        "differential"=>[
            Dict("testcd"=>"dr_b",   "orres"=>["r_bdt"]),
            Dict("testcd"=>"dc_i",   "orres"=>["(k_uptake*G-k_consumption*V*(10^15))"]),
            Dict("testcd"=>"dr_os",  "orres"=>["r_osdt"]),
            Dict("testcd"=>"dr",     "orres"=>["rdt"]),
            Dict("testcd"=>"dR_ref", "orres"=>["R_refdt"]),
            Dict("testcd"=>"dpi_t",  "orres"=>["E*2*d/(1-nu)*(rdt/r^2-R_refdt/(R_ref*r))", "-rdt/r*pi_t"])
        ]
    )

    initialValues = [
        Dict("testcd"=>"r_b"   ,"orres"=>"0.496161324363"),
        Dict("testcd"=>"c_i"   ,"orres"=>"0.00000000000638904517734"),
        Dict("testcd"=>"r_os"  ,"orres"=>"1.18773900649"),
        Dict("testcd"=>"r"     ,"orres"=>"1.68390033085"),
        Dict("testcd"=>"R_ref" ,"orres"=>"1.36108685239"),
        Dict("testcd"=>"pi_t"  ,"orres"=>"200000.0"),
    ]

    parameters = [
        Dict("testcd"=>"nu"                 ,"orres"=>"0.5"),
        Dict("testcd"=>"modulus_adjustment" ,"orres"=>"(1 - nu ^ 2) ^ (-1)"),
        Dict("testcd"=>"T"                  ,"orres"=>"303.15"),
        Dict("testcd"=>"pi_e"               ,"orres"=>"604594.08"),
        Dict("testcd"=>"phi"                ,"orres"=>"0.0001"),
        Dict("testcd"=>"k_consumption"      ,"orres"=>"0.00000000000000025"),
        Dict("testcd"=>"Lp"                 ,"orres"=>"0.00000119"),
        Dict("testcd"=>"d"                  ,"orres"=>"0.115"),
        Dict("testcd"=>"E_3D"               ,"orres"=>"2580000.0"),
        Dict("testcd"=>"c_e"                ,"orres"=>"240"),
        Dict("testcd"=>"E"                  ,"orres"=>"modulus_adjustment * E_3D"),
        Dict("testcd"=>"k_uptake"           ,"orres"=>"0.0000000000000002"),
        Dict("testcd"=>"pi_c"               ,"orres"=>"200000.0"),
        Dict("testcd"=>"R"                  ,"orres"=>"8.314"),
        Dict("testcd"=>"F"                  ,"orres"=>"96485")
    ]

    res = simulate(model, initialValues, parameters, [], start, stop, step_size, noise_level, seed)

    return res
end

function staticVolumeSimulation()
    initialValues = [
        0.496161324363,            # r_b
        0.00000000000638904517734, # c_i
        1.18773900649,             # r_os
        1.68390033085,             # r
        1.36108685239,             # R_ref
        200000.0                   # pi_t
    ]

    parameters = [
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
      du[1] = noise_level
      du[2] = noise_level
      du[3] = noise_level
      du[4] = noise_level
      du[5] = noise_level
      du[6] = noise_level
    end


    prob = SDEProblem(diff,noise,initialValues,(start,stop),parameters,seed=seed)

    res = diffeq_fd(prob.p,sol->sol[1:6,:],66,prob,SOSRI(),saveat=step_size)

    return Dict(
        "r_b"   => res[1, :],
        "c_i"   => res[2, :],
        "r_os"  => res[3, :],
        "r"     => res[4, :],
        "R_ref" => res[5, :],
        "pi_t"  => res[6, :]
    )
end

function testVolumeSimulation()
    dyn_res = dynamicVolumeSimulation()
    @show dyn_res

    sta_res = staticVolumeSimulation()
    @show sta_res

    @test dyn_res == sta_res
end

