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
termMatrix = ["+3*x" "-2*y"; "+4*y" "-x"]

# TODO: make the neuronal network matrix dynamically
neuronalNetworkMatrix = [[0 1]; [1 1]]

# create activated term matrix 
activatedTermMatrix = fill("",size(termMatrix)[1])
for row = 1:size(termMatrix,2)  
  for column = 1:size(termMatrix,1)
    # if the term is allowed
    if neuronalNetworkMatrix[row,column] == 1
      # add strings with '*' together  
      activatedTermMatrix[row] *= termMatrix[row,column]
    end
  end
end

# re-unit the variable matrix with their terms and precompile the equations
expressionMatrix = [Meta.parse(string(variableMatrix[i], "=" ,activatedTermMatrix[i])) for i in 1:myArraySize]

# testX = ["dx = σ*(y-x)"; "dy = x*(ρ-z)" ; "dz = x*y - β*z"]
# expressionMatrixTest = [Meta.parse(testX[i]) for i in 1:3]

function parameterized_lorenz(du,u,p,t)
  global x,y,z = u

  for j = 1:myArraySize
    eval(expressionMatrix[j])
  end

  # for better performance 
  du[1] = σ*(u[2]-u[1])
  du[2] = u[1]*(ρ-u[3]) - u[2]
  du[3] = u[1]*u[2] - β*u[3]
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
problem = SDEProblem(parameterized_lorenz, noiseModelSystem, initialValues, timeRange)#, seed=1234)#, noise=choosenNoise)

# solve the problem
sol = solve(problem)

# check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)#, save_everystep=false)

# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")

# # 3d plot
# plot(sol,vars=(1,2,3))