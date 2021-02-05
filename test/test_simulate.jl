using Test
using DifferentialEquations, DiffEqFlux
using Simulation


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

