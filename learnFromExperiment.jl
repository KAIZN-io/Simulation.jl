"""learn from experimental data --> DoE with simulation and experimental data"""


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
# include("/Users/janpiotraschke/GithubRepository/ProjectQ/learnFromExperiment.jl")

using Pkg

# Pkg.add("DifferentialEquations")
# Pkg.add("Plots")
# Pkg.add("BenchmarkTools")
# Pkg.add("Logging")
# Pkg.add("JuMP")

# using DifferentialEquations, BenchmarkTools
# using Plots; plotly()
# using Logging
# Flux is the neural network framework
# Flux finds the parameters of the neural network (p) which minimize the cost function
using Flux, DiffEqFlux, DifferentialEquations, Plots, Logging
# using BSON: @save

# using JuMP
# # set constraints to a matrice
# m = Model()
# @defVar(m, x[1:2] >= 0)
# c= [8 12]
# @setObjective(m, Max, sum([c[i]*x[i] for i= 1:2]))
# A=[6 8 ; 10 20]
# B= [72 140]' #bounds
# for j=1:2
#     @addConstraint(m,sum([A[j,i]*x[i] for i=1:2])<=B[j])
# end


solTest =[[1.01, 1.0], 
 [1.15528, 0.680492],
 [1.39068, 0.48099] ,
 [1.72764, 0.359908],
 [2.1866, 0.291497] ,
 [2.79419 ,0.26255] ,
 [3.57813, 0.271627],
 [4.55065, 0.335325],
 [5.66086 ,0.510012],
 [6.64364 ,0.964492],
 [6.71378, 2.06529] ,
 [5.05887 ,3.77483] ,
 [2.88214, 4.5484]  ,
 [1.65538, 3.86005] ,
 [1.14979, 2.78251] ,
 [0.977652 ,1.88232],
 [0.96849 ,1.25249] ,
 [1.06369 ,0.840986],
 [1.24811, 0.580706],
 [1.52646, 0.419878],
 [1.9144 ,0.324459] ,
 [2.43549 ,0.274401],
 [3.11798 ,0.261622],
 [3.98351, 0.292666],
 [5.03276 ,0.393955],
 [6.13847, 0.660282],
 [6.84915, 1.34796] ,
 [6.1777 ,2.81142]  ,
 [4.02848 ,4.32292] ,
 [2.22002 ,4.35864] ,
 [1.37617 ,3.38124] ,
 [1.0499, 2.35236]  ,
 [0.961345, 1.57433],
 [1.00191, 1.04957] ,
 [1.13686 ,0.712363],
 [1.36161, 0.50108] ,
 [1.68616, 0.372348],
 [2.12997, 0.298619],
 [2.71908, 0.265464],
 [3.48145, 0.269963],
 [4.42711, 0.329609],
 [5.53357, 0.485208],
 [6.54085, 0.895883],
 [6.76262 ,1.90421] ,
 [5.29173, 3.58941] ,
 [3.08894, 4.52542] ,
 [1.75548, 3.95983] ,
 [1.19262, 2.8935]  ,
 [0.994033 ,1.96846],
 [0.970674, 1.31208],
 [1.05568 ,0.880433]]


""" temporary experimental data handling

convert from a `Vector{Vector{Float64}}` to a `Vector{Float64, 2}`
--> with that the array of the sde solution and the data have the same type
"""

testSol = hcat(solTest...)[1,:]



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

# start:step:stop
t = timeRange[1]:0.2:timeRange[2]

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

# create activated term matrix 
activatedTermMatrix = fill("",size(termMatrix)[1])
for row in 1:myArraySize
  for column in 1:maxTermCount
    if neuronalNetworkMatrix[row,column] == 1
      # add strings with '*' together
      activatedTermMatrix[row,1] *= termMatrix[row,column]
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
noiseModelSystem(du,u,p,t) = @.(du = 0.01)

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
