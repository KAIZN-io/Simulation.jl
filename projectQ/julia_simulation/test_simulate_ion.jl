using Test

include("simulate.jl")

start = 0.0
stop = 1.0
step_size = 0.1
noise_level = 0.0
seed = 1337

function dynamicIonSimulation()
    initialValues = [
        Dict("testcd"=>"H_in"     ,"orres"=>"0.003063"),
        Dict("testcd"=>"K_in"     ,"orres"=>"75.54"),
        Dict("testcd"=>"Cl_in"    ,"orres"=>"0.545"),
        Dict("testcd"=>"Na_in"    ,"orres"=>"29.98"),
        Dict("testcd"=>"H_out"    ,"orres"=>"0.003162"),
        Dict("testcd"=>"K_out"    ,"orres"=>"0.1"),
        Dict("testcd"=>"Cl_out"   ,"orres"=>"0.1"),
        Dict("testcd"=>"Na_out"   ,"orres"=>"0.01"),
        Dict("testcd"=>"ATP"      ,"orres"=>"2.477"),
        Dict("testcd"=>"Deltaphi" ,"orres"=>"-0.168"),
        Dict("testcd"=>"L_ArH"    ,"orres"=>"0"),
        Dict("testcd"=>"L_HH"     ,"orres"=>"0.0000000016200000000000002")
    ]

    parameters = [
        Dict("testcd"=>"ATP_stimulus" ,"orres"=>"2.5"),
        Dict("testcd"=>"V_out"        ,"orres"=>"0.00000285"),
        Dict("testcd"=>"V_in"         ,"orres"=>"0.000000000018"),
        Dict("testcd"=>"Surf"         ,"orres"=>"0.0000229"),
        Dict("testcd"=>"pbc"          ,"orres"=>"200"),
        Dict("testcd"=>"C_m"          ,"orres"=>"0.01"),
        Dict("testcd"=>"c_strich_ATP" ,"orres"=>"0.316"),
        Dict("testcd"=>"K_eq"         ,"orres"=>"0.000001"),
        Dict("testcd"=>"L_HHaG"       ,"orres"=>"0.0019"),
        Dict("testcd"=>"L_ArHaG"      ,"orres"=>"-0.00195"),
        Dict("testcd"=>"L_HNa"        ,"orres"=>"-0.00000000000000631"),
        Dict("testcd"=>"L_NaH"        ,"orres"=>"-0.00000000000000631"),
        Dict("testcd"=>"L_KK"         ,"orres"=>"0.0000000000637"),
        Dict("testcd"=>"L_HCl"        ,"orres"=>"0.000000001298"),
        Dict("testcd"=>"L_ClH"        ,"orres"=>"0.000000001298"),
        Dict("testcd"=>"L_NaNa"       ,"orres"=>"0.00000000000000303"),
        Dict("testcd"=>"L_ClCl"       ,"orres"=>"0.0000000010400000000000001"),
        Dict("testcd"=>"L_HK"         ,"orres"=>"-0.00000000000000020720970439999999"),
        Dict("testcd"=>"L_KH"         ,"orres"=>"-0.00000000000000020720970439999999"),
        Dict("testcd"=>"k_incrHH"     ,"orres"=>"0.00000000354"),
        Dict("testcd"=>"k_incrArH"    ,"orres"=>"-0.0000000036400000000000003"),
        Dict("testcd"=>"k_ATPincr"    ,"orres"=>"10"),
        Dict("testcd"=>"k_ATPdecr"    ,"orres"=>"k_ATPincr / ATP_stimulus"),
        Dict("testcd"=>"k_decrArH"    ,"orres"=>"k_incrArH / L_ArHaG"),
        Dict("testcd"=>"k_decrHH"     ,"orres"=>"k_incrHH / L_HHaG"),
        Dict("testcd"=>"T"            ,"orres"=>"303.15"),
        Dict("testcd"=>"R"            ,"orres"=>"8.314"),
        Dict("testcd"=>"F"            ,"orres"=>"96485")
    ]

    model = Dict(
        "algebraic"=>[
            Dict(
                "testcd" => "A_Ar",
                "orres"  => [
                    "+(R*T/(c_strich_ATP))*(ATP-c_strich_ATP)*(1+K_eq)"
                ]
            ),
            Dict(
                "testcd" => "J_H",
                "orres"  => [
                    "+R*T*(L_HH*log(H_in/H_out))",
                    "+R*T*(L_HCl*log(Cl_in/Cl_out))",
                    "+R*T*(L_HK*log(K_in/K_out))",
                    "-L_ArH*A_Ar",
                    "+R*T*(L_HNa*log(Na_in/Na_out))",
                    "+F*Deltaphi*(L_HH+L_HK+L_HNa-L_HCl)"
                ]
            ),
            Dict(
                "testcd" => "J_Cl",
                "orres"  => [
                    "+R*T*(L_ClCl*log(Cl_in/Cl_out))",
                    "+R*T*(L_ClH*log(H_in/H_out))",
                    "+F*Deltaphi*(L_ClH-L_ClCl)"
                ]
            ),
            Dict(
                "testcd" => "J_K",
                "orres"  => [
                    "+R*T*(L_KH*log(H_in/H_out))",
                    "+F*Deltaphi*(L_KH+L_KK)",
                    "+R*T*(L_KK*log(K_in/K_out))"
                ]
            ),
            Dict(
                "testcd" => "J_Na",
                "orres"  => [
                    "+R*T*(L_NaNa*log(Na_in/Na_out))",
                    "+F*Deltaphi*(L_NaH+L_NaNa)",
                    "+R*T*(L_NaH*log(H_in/H_out))"
                ]
            )
        ],
        "differential" => [
            Dict(
                "testcd" => "dH_in",
                "orres"  =>["-(J_H*Surf*log(10)*H_in)/(V_in*pbc)"],
            ),
            Dict(
                "testcd" => "dK_in",
                "orres"  =>["-(J_K*Surf)/V_in"],
            ),
            Dict(
                "testcd" => "dCl_in",
                "orres"  =>["-(J_Cl*Surf)/V_in"]
            ),
            Dict(
                "testcd" => "dNa_in",
                "orres"  =>["-(J_Na*Surf)/V_in"],
            ),
            Dict(
                "testcd" => "dH_out",
                "orres"  =>["+(J_H*Surf)/V_out"],
            ),
            Dict(
                "testcd" => "dK_out",
                "orres"  =>["+(J_K*Surf)/V_out"],
            ),
            Dict(
                "testcd" => "dCl_out",
                "orres"  =>["+(J_Cl*Surf)/V_out"],
            ),
            Dict(
                "testcd" => "dNa_out",
                "orres"  =>["+(J_Na*Surf)/V_out"],
            ),
            Dict(
                "testcd" => "dATP",
                "orres"  =>["-k_ATPdecr*ATP", "+k_ATPincr"],
            ),
            Dict(
                "testcd" => "dDeltaphi",
                "orres"  =>["-(2*F/C_m)*(J_H+J_K+J_Na-J_Cl)"],
            ),
            Dict(
                "testcd" => "dL_ArH",
                "orres"  =>["+k_incrArH", "-k_decrArH*L_ArH"],
            ),
            Dict(
                "testcd" => "dL_HH",
                "orres"  =>["-k_decrHH*L_HH", "+k_incrHH"],
            )
        ]
    )

    res = simulate(model, initialValues, parameters, [], start, stop, step_size, noise_level, seed)

    return res
end

function staticIonSimulation()
    initialValues = [
        0.003063,                   # H_in
        75.54,                      # K_in
        0.545,                      # Cl_in
        29.98,                      # Na_in
        0.003162,                   # H_out
        0.1,                        # K_out
        0.1,                        # Cl_out
        0.01,                       # Na_out
        2.477,                      # ATP
        -0.168,                     # Deltaph
        0,                          # L_ArH
        0.0000000016200000000000002 # L_HH
    ]

    parameters = [
        2.5,                                 # ATP_stimulus
        0.00000285,                          # V_out
        0.000000000018,                      # V_in
        0.0000229,                           # Surf
        200,                                 # pbc
        0.01,                                # C_m
        0.316,                               # c_strich_ATP
        0.000001,                            # K_eq
        0.0019,                              # L_HHaG
        -0.00195,                            # L_ArHaG
        -0.00000000000000631,                # L_HNa
        -0.00000000000000631,                # L_NaH
        0.0000000000637,                     # L_KK
        0.000000001298,                      # L_HCl
        0.000000001298,                      # L_ClH
        0.00000000000000303,                 # L_NaNa
        0.0000000010400000000000001,         # L_ClCl
        -0.00000000000000020720970439999999, # L_HK
        -0.00000000000000020720970439999999, # L_KH
        0.00000000354,                       # k_incrHH
        -0.0000000036400000000000003,        # k_incrArH
        10,                                  # k_ATPincr
        303.15,                              # T
        8.314,                               # R
        96485                                # F
    ]

    function diff(du, values, parameters, time)
        # initial values
        H_in, K_in, Cl_in, Na_in, H_out, K_out, Cl_out, Na_out, ATP, Deltaphi,
        L_ArH, L_HH = values

        # Parameters
        ATP_stimulus, V_out, V_in, Surf, pbc, C_m, c_strich_ATP, K_eq, L_HHaG,
        L_ArHaG, L_HNa, L_NaH, L_KK, L_HCl, L_ClH, L_NaNa, L_ClCl, L_HK, L_KH,
        k_incrHH, k_incrArH, k_ATPincr, T, R, F = parameters
        k_ATPdecr = k_ATPincr / ATP_stimulus
        k_decrArH = k_incrArH / L_ArHaG
        k_decrHH  = k_incrHH / L_HHaG

        # algebraic equations
        A_Ar =
            +(R*T/(c_strich_ATP))*(ATP-c_strich_ATP)*(1+K_eq)
        J_H =
            +R*T*(L_HH*log(H_in/H_out))
            +R*T*(L_HCl*log(Cl_in/Cl_out))
            +R*T*(L_HK*log(K_in/K_out))
            -L_ArH*A_Ar
            +R*T*(L_HNa*log(Na_in/Na_out))
            +F*Deltaphi*(L_HH+L_HK+L_HNa-L_HCl)
        J_Cl =
            +R*T*(L_ClCl*log(Cl_in/Cl_out))
            +R*T*(L_ClH*log(H_in/H_out))
            +F*Deltaphi*(L_ClH-L_ClCl)
        J_K =
            +R*T*(L_KH*log(H_in/H_out))
            +F*Deltaphi*(L_KH+L_KK)
            +R*T*(L_KK*log(K_in/K_out))
        J_Na =
            +R*T*(L_NaNa*log(Na_in/Na_out))
            +F*Deltaphi*(L_NaH+L_NaNa)
            +R*T*(L_NaH*log(H_in/H_out))

        # calculate du
        du[1]  = dH_in     = -(J_H*Surf*log(10)*H_in)/(V_in*pbc)
        du[2]  = dK_in     = -(J_K*Surf)/V_in
        du[3]  = dCl_in    = -(J_Cl*Surf)/V_in
        du[4]  = dNa_in    = -(J_Na*Surf)/V_in
        du[5]  = dH_out    = +(J_H*Surf)/V_out
        du[6]  = dK_out    = +(J_K*Surf)/V_out
        du[7]  = dCl_out   = +(J_Cl*Surf)/V_out
        du[8]  = dNa_out   = +(J_Na*Surf)/V_out
        du[9]  = dATP      = -k_ATPdecr*ATP +k_ATPincr
        du[10] = dDeltaphi = -(2*F/C_m)*(J_H+J_K+J_Na-J_Cl)
        du[11] = dL_ArH    = +k_incrArH -k_decrArH*L_ArH
        du[12] = dL_HH     = -k_decrHH*L_HH +k_incrHH
    end

    function noise(du,u,p,t)
        du[1] = noise_level
        du[2] = noise_level
        du[3] = noise_level
        du[4] = noise_level
        du[5] = noise_level
        du[6] = noise_level
        du[7] = noise_level
        du[8] = noise_level
        du[9] = noise_level
        du[10] = noise_level
        du[11] = noise_level
        du[12] = noise_level
    end


    prob = SDEProblem(diff,noise,initialValues,(start,stop),parameters,seed=seed)
    @info prob

    res = diffeq_fd(prob.p,sol->sol[1:12,:],132,prob,SOSRI(),saveat=step_size)

    return Dict(
        "H_in"     => res[1, :],
        "K_in"     => res[2, :],
        "Cl_in"    => res[3, :],
        "Na_in"    => res[4, :],
        "H_out"    => res[5, :],
        "K_out"    => res[6, :],
        "Cl_out"   => res[7, :],
        "Na_out"   => res[8, :],
        "ATP"      => res[9, :],
        "Deltaphi" => res[10, :],
        "L_ArH"    => res[11, :],
        "L_HH"     => res[12, :]
    )
end

function testIonSimulation()
    dyn_res = dynamicIonSimulation()
    @show dyn_res

    sta_res = staticIonSimulation()
    @show sta_res

    verboseCompare(dyn_res, sta_res)
    @test dyn_res == sta_res
end

function verboseCompare(a, b)
    for (key, aValues) in a
        if ! haskey(b, key)
            @error string("b has no key '", key, "'.")
        end

        bValues = b[key]

        if length(aValues) != length(bValues)
            @error "a and b are not the same lenght."
        end

        for i in 1:length(aValues)
            if !(aValues[i] ≈ bValues[i])
                @error string("Values (", aValues[i], ", ", bValues[i], ") for key '", key, "' at index '", i, "' do not match.")
            end
        end
    end
end

