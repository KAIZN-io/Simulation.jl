"""learn from experimental data --> DoE with simulation and experimental data"""

using Pkg

# include("/Users/janpiotraschke/GithubRepository/ProjectQ/learnFromExperiment2.jl")
# import Pkg; Pkg.add("Flux")
# import Pkg; Pkg.add("DiffEqFlux")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("BSON")
# Pkg.add("ForwardDiff")
# Pkg.add("Documenter")
# Flux is the neural network framework
# Flux finds the parameters of the neural network (p) which minimize the cost function

#"""for LoadError --> rebuild Package / GR"""
# ENV["GRDIR"]=""
# Pkg.build("GR")

using Flux, DiffEqFlux, DifferentialEquations, Plots, Logging, Documenter
using ForwardDiff, LinearAlgebra
# using BSON: @save

"""intresting julia package

JuMP --> Modeling language for Mathematical Optimization; for constraints
Documenter --> A documentation generator for Julia.
Optim --> Optimization functions for Julia
StaticArrays --> Statically sized arrays for Julia
"""


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

# # transpose it with `'` 
# solTesttracked =hcat(solTest...)'

# The DEDataArray{T} type allows one to add other "non-continuous" variables to an array
mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end

# choose a solver: SOSRI(), Tsit5()
choosenSolver = SOSRI()

# get the parameter for the model
myParameterList = ["σ=10.0", "ρ=28.0", "β=8/3"]

# matrix with the variables name
variableMatrix = ["e"; "d"; "dx"; "dy"; "dz"]

# array of arrays 
inputTermArray = Array[["+3*x", "-2*y"], ["+4*y", "-x"], ["+σ*y", "-σ*x"], ["+x*ρ" ,"-x*z" ,"- y"], ["+x*y" ,"- β*z"]]

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

# impuls events
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

# create the raw vectors for the NN matrix as the NN layer 
rawValuesForNN = vcat(neuronalNetworkMatrix...)
rawVariablesForNN = vcat(neuronalNetworkMatrixVariable...)

# initialize the vectors for NN for value == 0 
valuesForNN = zeros(0)
variablesForNN = String[]

# reduce the vectors for NN for value == 0 
for i in 1:size(rawValuesForNN)[1]
  if rawValuesForNN[i] == 1
    append!(valuesForNN,rawValuesForNN[i])
    push!(variablesForNN,rawVariablesForNN[i])
  end
end


# re-unite the variable matrix with their terms and precompile the equations
expressionMatrix = [Meta.parse(string(variableMatrix[i], "=" ,activatedTermMatrix[i])) for i in 1:myArraySize]

@info "expression matrix for terms is created successfully"

function evalExpressionForSolver(u,du,p)
  
  for i = 1:size(valuesForNN)[1]

    # assign the NN parameter to their values
    eval(Meta.parse(string(variablesForNN[i], "=", p[i])))

  end

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
function lotka_volterra(du,u,p,t)
    evalExpressionForSolver(u,du,p)
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
prob = SDEProblem(lotka_volterra, noiseModelSystem, initialValues, timeRange, valuesForNN, seed=1234)#, noise=choosenNoise)
@info "start of the simulation"

# sol = solve(prob,Tsit5(),callback = cbs, tstops=tstop)
# plot(sol, linewidth=3,title="Solution of the SDE system")

"""Initial Parameter Vector 

which will be changed by the training algorithm.

The param function converts a normal Julia array into a new object that, while 
behaving like an array, tracks extra information that allows us to calculate 
derivatives
"""
neuralParameter = param(valuesForNN)


"""
Next we define a single layer neural network that uses the diffeq_rd (for ODE)
or a diffeq_fd (for SDE) layer function that takes the parameters and 
returns the solution of the x(t) variable
"""
function predict_fd_sde()
  # # diffeq_fd(p,sol->sol[1,:],101,prob,SOSRI(),saveat=0.1)
  diffeq_fd(neuralParameter,sol->sol[1,:],51,prob,choosenSolver,saveat=t)
end

"""cost function

use a predifined loss function or calculate however you want

now: calculate the sum of the absolute squares of the entries of 
      a vector v: sum(abs2,v)

erklaerung: 
predict_rd().u / predict_fd_sde() entspricht den Variablen Werten des Fits
solTest / testSol sind die Messwerte
man nimmt die Differenz von den Messpunkten des gleichen Zeitpunkt...
und dreht die Matrix um 90 Grad mittels hcat(Matrix...), damit sum(abs2,Matrix)
damit rechnen kann

einschraenkung:
momentan müssen die Messwerte die gleichen Zeitpunkte besitzen.
"""

loss_fd_sde() = sum(abs2,hcat((predict_fd_sde() - testSol)))
# loss(x,y) = Flux.mse(predict_fd_sde(),testSol)

# run n iteration
data = Iterators.repeated((), 10)

opt = ADAM(0.1)

# callback function to observe training
cb = function ()
  # @show loss_fd_sde()
  @info "alles ok am Anfang von cb"

  """ Infos about the solver

  returns = n-element Array{Array{Float64,1},1}
  saveat: Denotes specific times to save the solution at
  maxiters: Maximum number of iterations before stopping. Defaults to 1e5.
  """
  # using `remake` to re-create our `prob` with current parameters `p`
  # NOTE: prob is correctly defined; remake is not the problem

  
  # ERROR: MethodError: Cannot `convert` an object of type Array{Float64,1} to an 
  # object of type SimType{Float64}

  # --> NOTE: typeof(Flux.data(neuralParameter)) == Array{Float64,1}
  
  odeData = solve(remake(prob,p=Flux.data(neuralParameter)),choosenSolver,saveat=t,maxiters = 1e5)
  #   odeData = solve(prob,p=Flux.data(neuralParameter),choosenSolver,saveat=t,maxiters = 1e5)

  @info "alles ok nach Loesen der Gleichungen"

  # display only the first ODE in the same figure as the data
  scatter(t,testSol,color=[1],label = "first ODE data")

  display(plot!(t,odeData[1,:],ylim=(0,10),label="fit"))

  @info "alles ok Ende Anfang von cb"
end

"""train function

3 Steps:
1. how good is our model with 
2. the given data
3. and how could we improve it by changing the parameters

Flux.train!(objective, params, data, opt)
objective: evaluates how well a model is doing given some input data.
opt: (optimiser) update the model parameters appropriately

Callbacks are called for every batch of training data. You can slow this down 
using Flux.throttle(f, timeout) which prevents f from being called more than 
once every timeout seconds.
"""

@info "alles ok vor Flux"

Flux.train!(loss_fd_sde, [neuralParameter], data, opt, cb = cb)


# @info "trained parameters:" neuralParameter


# # # # You may wish to save models so that they can be loaded and run in a later 
# # # # session. The easiest way to do this is via BSON.jl.
# # # # @save "mymodel.bson" neuralParameter
