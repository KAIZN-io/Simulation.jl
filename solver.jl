"""copy paste this code into the terminal"""
# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("ParameterizedFunctions")


using ParameterizedFunctions
using DifferentialEquations
using Plots; plotly()


# defining our ODE system as parameterized functions
function modelSystem(du,u,p,t)
 du[1] = p[1]*(u[2]-u[1])
 du[2] = u[1]*(p[2]-u[3]) - u[2]
 du[3] = u[1]*u[2] - p[3]*u[3]
end


# modelSystem = @ode_def_bare modelSystem begin
#     dx = σ*(y-x)
#     dy = x*(ρ-z) - y
#     dz = x*y - β*z
# end σ ρ β

# defining our noise as parameterized functions
noiseModelSystem(du,u,p,t) = @.(du = 3.0)

# define the initial Values --> vector 
initialValues=[1.0,0.0,0.0]

# define the parameters --> vector
parameter=[10.0,28.0,8/3]

# time array (must be a tuple)
timeRange = (0.0,2.0)

# # change the Gaussian white noise
# choosenNoise = WienerProcess(0.0,0.0,0.0)

# define the Problem  -->  Gaussian white noise is default
# set the seed for reproducing the same stochastic simulation
problem = SDEProblem(modelSystem, noiseModelSystem, initialValues, timeRange, parameter, seed=1234)#, noise=choosenNoise)

# solve the problem
sol = solve(problem)

# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")

# 3d plot
# plot(sol,vars=(1,2,3))


