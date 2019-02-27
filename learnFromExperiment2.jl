"""learn from experimental data --> DoE with simulation and experimental data"""

"""You can remove all the package stuff with `rm -fr .julia`

for LoadError --> rebuild Package / GR: 
ENV["GRDIR"]=""
Pkg.build("GR")
"""


# include("/Users/janpiotraschke/GithubRepository/ProjectQ/learnFromExperiment2.jl")

"""intresting julia package

JuMP --> Modeling language for Mathematical Optimization; for constraints
Documenter --> A documentation generator for Julia.
Optim --> Optimization functions for Julia
StaticArrays --> Statically sized arrays for Julia
"""

using Pkg

# Pkg.add("Flux")
# Pkg.add("DiffEqFlux")
# Pkg.add("DifferentialEquations")
# Pkg.add("Plots")
# Pkg.add("Logging")
# Pkg.add("Documenter")

using Flux, DiffEqFlux, DifferentialEquations, Plots, Logging


solTest =[[1.01, 1.0, 1.0], 
 [1.15528, 0.680492, 1.0],
 [1.39068, 0.48099, 1.0] ,
 [1.72764, 0.359908, 1.0],
 [2.1866, 0.291497, 1.0] ,
 [2.79419 ,0.26255, 1.0] ,
 [3.57813, 0.271627, 1.0],
 [4.55065, 0.335325, 1.0],
 [5.66086 ,0.510012, 1.0],
 [6.64364 ,0.964492, 1.0],
 [6.71378, 2.06529, 1.0] ,
 [5.05887 ,3.77483, 1.0] ,
 [2.88214, 4.5484, 1.0]  ,
 [1.65538, 3.86005, 1.0] ,
 [1.14979, 2.78251, 1.0] ,
 [0.977652 ,1.88232, 1.0],
 [0.96849 ,1.25249, 1.0] ,
 [1.06369 ,0.840986, 1.0],
 [1.24811, 0.580706, 1.0],
 [1.52646, 0.419878, 1.0],
 [1.9144 ,0.324459, 1.0] ,
 [2.43549 ,0.274401, 1.0],
 [3.11798 ,0.261622, 1.0],
 [3.98351, 0.292666, 1.0],
 [5.03276 ,0.393955, 1.0],
 [6.13847, 0.660282, 1.0],
 [6.84915, 1.34796, 1.0] ,
 [6.1777 ,2.81142, 1.0]  ,
 [4.02848 ,4.32292, 1.0] ,
 [2.22002 ,4.35864, 1.0] ,
 [1.37617 ,3.38124, 1.0] ,
 [1.0499, 2.35236, 1.0]  ,
 [0.961345, 1.57433, 1.0],
 [1.00191, 1.04957, 1.0] ,
 [1.13686 ,0.712363, 1.0],
 [1.36161, 0.50108, 1.0] ,
 [1.68616, 0.372348, 1.0],
 [2.12997, 0.298619, 1.0],
 [2.71908, 0.265464, 1.0],
 [3.48145, 0.269963, 1.0],
 [4.42711, 0.329609, 1.0],
 [5.53357, 0.485208, 1.0],
 [6.54085, 0.895883, 1.0],
 [6.76262 ,1.90421, 1.0] ,
 [5.29173, 3.58941, 1.0] ,
 [3.08894, 4.52542, 1.0] ,
 [1.75548, 3.95983, 1.0] ,
 [1.19262, 2.8935, 1.0]  ,
 [0.994033 ,1.96846, 1.0],
 [0.970674, 1.31208, 1.0],
 [1.05568 ,0.880433, 1.0]]


""" temporary experimental data handling

convert from a `Vector{Vector{Float64}}` to a `Vector{Float64, 2}`
--> with that the array of the sde solution and the data have the same type
"""

testSol = hcat(solTest...)[1,:]


"""A struct can declare an abstract super type via <: syntax
Subtype operator: returns true if and only if all values of type T1 are also of type T2.

julia> Float64 <: AbstractFloat
true

Use mutable struct to declare a type whose instances can be modified

type restrictions with '::'
"""

mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end

# choose a solver: SOSRI(), Tsit5()
choosenSolver = SOSRI()

# run n iteration
nIteration = 10

# get the parameter for the model
myParameterList = ["σ=10.0", "ρ=28.0", "β=8/3"]

# matrix with the variables name
variableMatrix = ["e"; "d"; "dx"; "dy"; "dz"]

# array of arrays 
inputTermArray = Array[["+3*x", "-2*y"], ["+4*y", "-x"], ["+σ*y", "-σ*x"], ["+x*ρ" ,"-x*z" ,"- y"], ["+x*y" ,"- β*z"]]
odeMatrix = Array[["+σ*y", "-σ*x"], ["+x*ρ" ,"-x*z" ,"- y"], ["+x*y" ,"- β*z"]]

# array with the ODEs
odeNames = ["dx", "dy", "dz"]
odeVariable = ["x", "y", "z"]

# define the initial Values --> [1*m] vector 
initialValuesList=[2.0;1.0;1.0]
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

# make the unmutable parameter global 
for i = 1:size(myParameterList)[1]
  ex = Meta.parse(myParameterList[i])
  eval(ex)
end

# preparation --> assign the equations to a dict 
equationDict = Dict()
for i = 1:size(variableMatrix)[1]
  equationDict[variableMatrix[i]] = inputTermArray[i]
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
emptyOdeMatrix = fill("", size(odeNames)[1], maxTermCount)

# fill the term matrix with the terms
termMatrix = fillTermMatrix(emptyTermMatrix,inputTermArray)
realOdeMatrix = fillTermMatrix(emptyOdeMatrix,odeMatrix)

# create the neuronal network matrix filled with ones
neuronalNetworkMatrix = ones(size(odeNames)[1],maxTermCount)

# create the parameters of the neural network --> copy the array dimensions
neuronalNetworkMatrixVariable = similar(neuronalNetworkMatrix, String)

# fill the neuronalNetworkMatrixVariable with the parameters
for row in 1:size(odeNames)[1]
  for column in 1:maxTermCount
    if realOdeMatrix[row,column] == ""
      neuronalNetworkMatrix[row,column] = 0
    end
    if neuronalNetworkMatrix[row,column] == 1
      # add strings with '*' together
      neuronalNetworkMatrixVariable[row,column] = "m"*string(row)*string(column)
      
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



@info "expression matrix for terms is created successfully"

function evalExpressionForSolver(u,du,placeHolder)

  # NOTE: momentan laeuft der NN Parameter Ansatz nicht!!!


  # evaluate the initial values 
  for i = 1:size(u)[1]
    strPosition = findlast("(", string(u[i]))

    # assumption: the initial value should always be in the first place of the tuple
    stringTuple = string(u[i])[strPosition[1]:end]

    initPlaceHolder = eval(Meta.parse(stringTuple))

    eval(Meta.parse(string(odeVariable[i],"=",initPlaceHolder[1])))
  end

  # eval the algebraic equations and sde
  for (key,value) in equationDict
    ex = Meta.parse(string(key, "=",sum([eval(Meta.parse(iterator)) for iterator in value])))
    eval(ex)
  end

  A = placeHolder
  
  # how long the vector is
  # why : size(placeHolder) = (9,) ???

  sizeA = size(rawValuesForNN)[1]
  
  # how long the vector should be
  B = resize!(A, sizeA)
  
  # reshape the matrix 
  NNMatrix = reshape(B, size(odeNames)[1], maxTermCount)
  
  # empty the matrix
  # NOTE: warum setzt fill! auch die placeHolder auf 0.0 ?
  # NNMatrix = fill!(NNMatrix, 0.0)

  # @show placeHolder[7]

  # iteration number for parameter Placeholder vector 
  iterNum = 1
  for j = 1:size(realOdeMatrix,2)
    for i = 1:size(realOdeMatrix,1)
        if realOdeMatrix[i,j] != ""
          ex =  Meta.parse(realOdeMatrix[i,j])

          # @show iterNum
          # @show placeHolder[iterNum]
          # calculate the solution of the NN affected Matrix 
          NNMatrix[i,j] = placeHolder[iterNum] * eval(ex)
          iterNum += 1
        else
          NNMatrix[i,j] = 0.0
        end
    end
  end

  
  iterNum = 1
  for i in odeNames
    du[iterNum] = sum(NNMatrix[iterNum,:])
    iterNum +=1
  end

  @show du
  @show dessd
  return du
end


# the sde system 
function lotka_volterra(du,u,p,t)
  
    placeHolder = p
    evalExpressionForSolver(u,du,placeHolder)
end

# define the noise
noiseModelSystem(du,u,p,t) = @.(du = 0.01)


# function condition(u,t,integrator)
#     t in tstop
# end

# function affect!(integrator)
#     # add the term to the ode
#     integrator.u[3] += stimulus
# end

# cb = DiscreteCallback(condition, affect!)
# # could be a set of callback
# cbs = CallbackSet(cb)


# change the Gaussian white noise
choosenNoise = WienerProcess(0.0,0.0,0.0)

# define the Problem  -->  Gaussian white noise is default
# set the seed for reproducing the same stochastic simulation --> seed=1234

prob = SDEProblem(lotka_volterra, noiseModelSystem, initialValues, timeRange, valuesForNN, seed=1234)#, noise=choosenNoise)


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

data = Iterators.repeated((), nIteration)

# optimize function 
opt = ADAM(0.1)

# callback function to observe training
cb = function ()
  @show loss_fd_sde()

  """ Infos about the solver

  returns = n-element Array{Array{Float64,1},1}
  saveat: Denotes specific times to save the solution at
  maxiters: Maximum number of iterations before stopping. Defaults to 1e5.
  """

  # sol = solve(prob,Tsit5(),callback = cbs, tstops=tstop)
  odeData = solve(remake(prob,p=Flux.data(neuralParameter)),choosenSolver,saveat=t,maxiters = 1e5)
  #   odeData = solve(prob,p=Flux.data(neuralParameter),choosenSolver,saveat=t,maxiters = 1e5)

  # display only the first ODE in the same figure as the data
  scatter(t,testSol,color=[1],label = "first ODE data")

  display(plot!(t,odeData[1,:],ylim=(0,10),label="fit"))

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


@info "trained parameters:" neuralParameter


# # You may wish to save models so that they can be loaded and run in a later 
# # session. The easiest way to do this is via BSON.jl.
# @save "mymodel.bson" neuralParameter
