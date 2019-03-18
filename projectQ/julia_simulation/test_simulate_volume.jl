using Test

include("simulate.jl")

start = 0.0
stop = 1.0
step_size = 0.1
noise_level = 0.0
seed = 1337

function dynamicVolumeSimulation()
    model = Dict(
        "algebraic"=>Dict(
            "R_refdt"=>["phi*R_ref*r/(2*d)*max(pi_t-pi_c,0)"],
            "r_bdt"=>["0.2*R_refdt"],
            "R_ref"=>["r/(1+(1-nu)*(pi_t*r)/(E*2*d))"],
            "V"=>["4/3*pi*10^(-15)*r^3"],
            "pi_i"=>["c_i/V*R*T"],
            "V_ref"=>["4/3*pi*10^(-15)*R_ref^3"],
            "G"=>["4*pi*r^2"],
            "r_osdt"=>["-Lp*(pi_t+pi_e-pi_i)"],
            "rdt"=>["0.2*R_refdt", "-Lp*(pi_t+pi_e-pi_i)"]
        ),
        "differential"=>Dict(
            "dr_b"=>["r_bdt"],
            "dc_i"=>["(k_uptake*G-k_consumption*V*(10^15))"],
            "dr_os"=>["r_osdt"],
            "dr"=>["rdt"],
            "dR_ref"=>["R_refdt"],
            "dpi_t"=>["E*2*d/(1-nu)*(rdt/r^2-R_refdt/(R_ref*r))", "-rdt/r*pi_t"]
        )
    )

    initialValues = Dict(
        "r_b"=>"0.496161324363",
        "c_i"=>"0.00000000000638904517734",
        "r_os"=>"1.18773900649",
        "r"=>"1.68390033085",
        "R_ref"=>"1.36108685239",
        "pi_t"=>"200000.0"
    )

    parameters = Dict(
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

