"""copy paste this code into the terminal"""

# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("ParameterizedFunctions")
# import Pkg; Pkg.add("BenchmarkTools")

using ParameterizedFunctions
using DifferentialEquations, BenchmarkTools
using Plots; plotly()


# get the parameter for the model
myParameterList = ["σ=10.0", "ρ=28.0", "β=8/3"]
σ=10.0
ρ=28.0
β=8/3
# make the parameter global 
# for i = 1:size(myParameterList)[1]
#     ex = Meta.parse(myParameterList[i])

#     # eval the expression in the function
#     eval(ex)
# end

# define the equation as a string in a list
myStringList = ["e = 3 * x - y", "c = 4 * y - x"]#, "dx = σ*(y-x) * e", "dy = x*(ρ-z) - y *c", "dz = x*y - β*z"]
# myStringList = ["e = 3 * x - y", "c = 4 * y - x", "dx = σ*(y-x) * e", "dy = x*(ρ-z) - y *c", "dz = x*y - β*z"]

# get the len of the array
myArraySize = size(myStringList)[1]

f_lorenz = @ode_def_bare LorenzSDE begin
  dx = σ*(y-x)
  dy = x*(ρ-z) - y
  dz = x*y - β*z
end 

termMatrix = [[1 2]; [3 4]]
neuronalNetworkMatrix = [[1 0]; [1 1]]

# Hadamard product .* of matrix 
activatedTermMatrix = termMatrix .* neuronalNetworkMatrix

# defining our noise as parameterized functions
noiseModelSystem(du,u,p,t) = @.(du = 3.0)

# define the initial Values --> [1*m] vector 
initialValues=[1.0;1.0;1.0]

# time array (must be a tuple)
timeRange = (0.0,2.0)

# # change the Gaussian white noise
# choosenNoise = WienerProcess(0.0,0.0,0.0)

# define the Problem  -->  Gaussian white noise is default
# set the seed for reproducing the same stochastic simulation
problem = SDEProblem(f_lorenz, noiseModelSystem, initialValues, timeRange)#, seed=1234)#, noise=choosenNoise)

# solve the problem
# sol = solve(problem)

# check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)#, save_everystep=false)

# plot the solution
# plot(sol, linewidth=3,title="Solution of the SDE system")

# # 3d plot
# plot(sol,vars=(1,2,3))