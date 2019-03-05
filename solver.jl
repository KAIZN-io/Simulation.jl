"""learn from simulation data --> DoE with simulation data"""


"""
Universal Approximation Theorem states that, for enough layers or enough parameters 
ML(x) can approximate any nonlinear function sufficiently close. 

In many cases we do not know the full nonlinear equation, but we may know 
details about its structure. 

So as our machine learning models grow and are hungry for larger and larger amounts 
of data, differential equations have become an attractive option for specifying
nonlinearities in a learnable (via the parameters) but constrained form.

They are essentially a way of incorporating prior domain-specific knowledge of 
the structural relations between the inputs and outputs.
"""

"""copy paste this code into the terminal"""
# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")

# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("BenchmarkTools")
# import Pkg; Pkg.add("Logging")

using DifferentialEquations, BenchmarkTools
using Plots#; plotly()
using Logging

# The DEDataArray{T} type allows one to add other "non-continuous" variables to an array
mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end

# get the parameter for the model
myParameterList = ["σ=10.0", "ρ=28.0", "β=8/3"]

# matrix with the variables name
variableMatrix = ["e"; "d"; "dx"; "dy"; "dz"]

# array of arrays 
inputTermArray = Array[["+3*x", "-2*y", "+2*z"], ["+4*y", "-x"], ["+σ*y", "-σ*x"], ["+x*ρ" ,"-x*z" ,"- y"], ["+x*y" ,"- β*z"]]

# array with the ODEs
odeNames = ["dx", "dy", "dz"]
odeVariable = ["x", "y", "z"]

# define the initial Values --> [1*m] vector 
initialValuesList=[1.0;1.0;1.0]
initialValues = SimType(initialValuesList, 0.0)

# time array (must be a tuple)
timeRange = (0.0,8.0)

tstop = [5.0;6.0]

# apply a stimulus value
stimulus = 10.5

# # # # # # # # # # # # 

# make the parameter global 
for i = 1:size(myParameterList)[1]
  ex = Meta.parse(myParameterList[i])
    eval(ex)
end

function getMaxTermCount(arrayTerms)
  maxTermCount = 0
  for row in eachindex(arrayTerms)
    arraySize = size(arrayTerms[row])[1]
    if arraySize > maxTermCount
      maxTermCount = arraySize
    end
  end
  return maxTermCount
end

function fillTermMatrix(fillMatrix, arrayTerms)
  for row in eachindex(arrayTerms)
    y = arrayTerms[row]
    for column in eachindex(y)
      fillMatrix[row,column] = y[column]
    end
  end  
  return fillMatrix 
end

# get the len of the array
myArraySize = size(variableMatrix)[1]

# get the maximal term count
maxTermCount = getMaxTermCount(inputTermArray)

# create the generel term matrix
emptyTermMatrix = fill("", myArraySize, maxTermCount)

# fill the term matrix with the terms
termMatrix = fillTermMatrix(emptyTermMatrix,inputTermArray)

# create the neuronal network matrix filled with ones
neuronalNetworkMatrix = ones(myArraySize,maxTermCount)

# create the parameters of the neural network
neuronalNetworkMatrixVariable = Array{String}(undef, myArraySize,maxTermCount)

# create activated term matrix 
activatedTermMatrix = fill("",size(termMatrix)[1])
for row in 1:myArraySize
  for column in 1:maxTermCount
    # set the NN matrix element to 0 / undef if term matrix does not hold any 
    # string in the same place
    if termMatrix[row,column] == ""
      neuronalNetworkMatrix[row,column] = 0
    end

    if neuronalNetworkMatrix[row,column] == 1
      # add strings with '*' together
      neuronalNetworkMatrixVariable[row,column] = "m"*string(column)*string(row)
      
      activatedTermMatrix[row,1] *= termMatrix[row,column] * "*"* neuronalNetworkMatrixVariable[row,column]
    else
       neuronalNetworkMatrixVariable[row,column] = ""
    end
  end
end  




# re-unite the variable matrix with their terms and precompile the equations
expressionMatrix = [Meta.parse(string(variableMatrix[i], "=" ,activatedTermMatrix[i])) for i in 1:myArraySize]

@info "expression matrix for terms is created successfully"

function evalExpressionForSolver(u,du)

  for i = 1:size(odeNames)[1]
    # convert the ODE names
    eval(Meta.parse(string(odeNames[i], "=", du[i])))

    # assign the initial values to their ODEs
    eval(Meta.parse(string(odeVariable[i], "=", u[i])))
  end

  # calculate the equations
  for j = 1:myArraySize
    eval(expressionMatrix[j])
  end

  # overgive only the d_ terms 
  for i = 1:size(odeNames)[1]
    du[i]= eval(Meta.parse(odeNames[i]))
  end

  return du
end

# the function for solving the SDE
function parameterized_lorenz(du,u,p,t)
  evalExpressionForSolver(u,du)
end

# defining our noise as parameterized functions
noiseModelSystem(du,u,p,t) = @.(du = 3.0)

function condition(u,t,integrator)
    t in tstop
end

function affect!(integrator)
    # add the term to the ode
    integrator.u[3] += stimulus
end

cb = DiscreteCallback(condition, affect!)
# could be a set of callback
cbs = CallbackSet(cb)


# change the Gaussian white noise
choosenNoise = WienerProcess(0.0,0.0,0.0)

# define the Problem  -->  Gaussian white noise is default
# set the seed for reproducing the same stochastic simulation --> seed=1234
problem = SDEProblem(parameterized_lorenz, noiseModelSystem, initialValues, timeRange, seed=1234)#, noise=choosenNoise)
@info "start of the simulation"

# solve the problem
# sol = solve(problem)
sol = solve(problem,Tsit5(),callback = cbs, tstops=tstop)

@info "the equation system is solved"

# check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)

# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")
