# include("/Users/janpiotraschke/GithubRepository/ProjectQ/test.jl")

using DifferentialEquations, BenchmarkTools
using Plots; plotly()
using Logging

# ContinuousCallback is applied when a continuous condition function hits zero
# A DiscreteCallback is applied when its condition function is true.

mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end

function f(du,u,p,t)
    du[1] = -0.5*u[1] + u.f1
    du[2] = -0.5*u[2]
end

function condition(u,t,integrator)
    t in tstop
end

function affect!(integrator)

    # add the term to the ode
    integrator.u[2] += 3.5
    # for c in full_cache(integrator)
    #     c.f1 += 3.5
    # end
end

save_positions = (true,true)

cb = DiscreteCallback(condition, affect!, save_positions=save_positions)

# could be a set of callback
cbs = CallbackSet(cb)

u0 = SimType([10.0;10.0], 0.0)
prob = ODEProblem(f,u0,(0.0,10.0))

tstop = [5.;6.]
# @benchmark sol = solve(prob,Tsit5(),callback = cbs, tstops=tstop)
sol = solve(prob,Tsit5(),callback = cbs, tstops=tstop)
plot(sol, linewidth=3,title="Solution of the SDE system")