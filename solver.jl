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

# make the parameter global 
for i = 1:size(myParameterList)[1]
    ex = Meta.parse(myParameterList[i])
    eval(ex)
end

# define the equation as a string in a list
myStringList = ["e = 3 * x - y", "c = 4 * y - x"]

# get the len of the array
myArraySize = size(myStringList)[1]

# matrix for test 
variableMatrix = ["e"; "d"]
termMatrix = ["+3*x" "-y"; "+4*y" "-x"]

# myStringList = ["e = 3 * x - y", "c = 4 * y - x", "dx = σ*(y-x) * e", "dy = x*(ρ-z) - y *c", "dz = x*y - β*z"]


# create activated term matrix 
activatedTermMatrix = fill("",size(termMatrix)[1])
for row = 1:size(termMatrix,2)  
  for column = 1:size(termMatrix,1)
    # add strings with '*' together 
    activatedTermMatrix[row] *= termMatrix[row,column]
    end
end

# NOTE: Further Work
# # our matrix for the construction of a neuronal network
# neuronalNetworkMatrix = [[1 0]; [1 1]]

# # Hadamard product .* of matrix 
# activatedTermMatrix = termMatrix .* neuronalNetworkMatrix

f_lorenz = @ode_def_bare LorenzSDE begin
  # for j = 1:myArraySize
  #     ex = Meta.parse(myStringList[j])
  #     eval(ex)
  # end

  dx = σ*(y-x)
  dy = x*(ρ-z) - y
  dz = x*y - β*z
end 


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
sol = solve(problem)

# check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)#, save_everystep=false)

# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")

# # 3d plot
# plot(sol,vars=(1,2,3))