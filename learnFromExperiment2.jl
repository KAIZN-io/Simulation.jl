# include("/Users/janpiotraschke/GithubRepository/ProjectQ/learnFromExperiment2.jl")

using Pkg

# Pkg.add("Flux")
# Pkg.add("DiffEqFlux")
# Pkg.add("DifferentialEquations")
# Pkg.add("Plots")
# Pkg.add("Logging")
# Pkg.add("Documenter")

using Flux, DiffEqFlux, DifferentialEquations, Plots, Logging
using Flux.Tracker

mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end

# get the 'experimental' data
include("/Users/janpiotraschke/GithubRepository/ProjectQ/testData.jl")

# temporary: assess the NN only with the first experimental data column
testSol = hcat(solTest...)[1,:]

# choose a solver: SOSRI(), Tsit5()
choosenSolver = SOSRI()

# run n iteration
nIteration = 100

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
initialValuesList=[1.01;1.0;1.0]
initialValues = SimType(initialValuesList, 0.0)

# time array (must be a tuple)
timeRange = (0.0,10.0)

# start:step:stop
t = timeRange[1]:0.2:timeRange[2]

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
    stringTuple = string(u[i])[strPosition[1]:end]
    
    initPlaceHolder = eval(Meta.parse(stringTuple))

    eval(Meta.parse(string(odeVariable[i],"=",initPlaceHolder[1])))
  end

  # eval the algebraic equations and sde
  for (key,value) in equationDict
    ex = Meta.parse(string(key, "=",sum([eval(Meta.parse(iterator)) for iterator in value])))
    eval(ex)
  end
  
  # copy is important to not change the original matrix
  A = copy(placeHolder)
  # @show typeof(placeHolder)

  # how long the vector is
  sizeA = size(rawValuesForNN)[1]
  
  # how long the vector should be
  B = resize!(A, sizeA)
  
  # reshape the matrix 
  NNMatrix = reshape(B, size(odeNames)[1], maxTermCount)
  
  # empty the matrix
  NNMatrix = fill!(NNMatrix, 0.0)
  
  # iteration number for parameter Placeholder vector 
  iterNum = 1
  for j = 1:size(realOdeMatrix,2)
    for i = 1:size(realOdeMatrix,1)
        if realOdeMatrix[i,j] != ""
          ex =  Meta.parse(realOdeMatrix[i,j])

          # calculate the solution of the NN affected Matrix 
          NNMatrix[i,j] = placeHolder[iterNum] * eval(ex)
          iterNum += 1
        end
    end
  end

  iterNum = 1
  for i in odeNames
    du[iterNum] = sum(NNMatrix[iterNum,:])
    iterNum +=1
  end

  # NOTE: (typeof(du) == typeof(placeHolder)) = true

  return du
end


# the sde system 
function lotka_volterra(du,u,p,t)

  evalExpressionForSolver(u,du,p)
  # @show dessd

end

# define the noise
noiseModelSystem(du,u,p,t) = @.(du = 0.01)

# define the Problem 
prob = SDEProblem(lotka_volterra, noiseModelSystem, initialValues, timeRange, valuesForNN, seed=1234)#, noise=choosenNoise)

"""Initial Parameter Vector
which will be changed by the training algorithm.
"""



neuralParameter = param(valuesForNN)


"""
Next we define a single layer neural network that uses the diffeq_rd (for ODE)
or a diffeq_fd (for SDE) layer function that takes the parameters and 
returns the solution of the x(t) variable
"""
  
function predict_fd_sde()

  diffeq_fd(neuralParameter,sol->sol[1,:],size(t)[1],prob,choosenSolver,saveat=t)
end

# cost function 
loss_fd_sde() = sum(abs2,hcat((predict_fd_sde() - testSol)))

# number of repeated simulations
data = Iterators.repeated((), nIteration)

# optimize function : (optimiser) update the model parameters appropriately
opt = ADAM(0.1)

# train! takes an additional argument, cb, that's used for callbacks so that you can observe the training process. 
# cb = function ()
#   @info "in the call-back function now"

#   display(loss_fd_sde())

#   """
#   normal :
#   u = ForwardDiff.Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##71#72")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64},Float64,7}[Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##71#72")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(-4.63278,-742.021,0.0,0.0,736.434,0.0,0.0,0.0), Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##71#72")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(-4.08654,0.0,-2062.02,0.0,0.0,1982.75,0.0,74.2021), Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##71#72")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(23.4783,0.0,0.0,725.325,0.0,0.0,-702.84,0.0)]

#   ┌ Info: SDEProblem with uType SimType{Float64} and tType Float64. In-place: true
#   │ timespan: (0.0, 10.0)
#   └ u0: [1.01, 1.0, 1.0]
#   p = ForwardDiff.Dual(.......)
#   du = ForwardDiff.Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##17#18")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64},Float64,7}[Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##17#18")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(6.01445,-112.855,0.0,0.0,97.8038,0.0,0.0,0.0), Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##17#18")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(36.5543,0.0,-273.851,0.0,0.0,299.119,0.0,11.2855), Dual{ForwardDiff.Tag{getfield(DiffEqFlux, Symbol("##5#10")){SimType{Float64},Base.Iterators.Pairs{Symbol,StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}},Tuple{Symbol},NamedTuple{(:saveat,),Tuple{StepRangeLen{Float64,Base.TwicePrecision{Float64},Base.TwicePrecision{Float64}}}}},getfield(Main, Symbol("##17#18")),SDEProblem{SimType{Float64},Tuple{Float64,Float64},true,Array{Float64,1},Nothing,SDEFunction{true,typeof(lotka_volterra),typeof(noiseModelSystem),LinearAlgebra.UniformScaling{Bool},Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing,Nothing},typeof(noiseModelSystem),Nothing,Nothing},Tuple{SOSRI}},Float64}}(28.8204,0.0,0.0,110.377,0.0,0.0,-81.5563,0.0)]

#   now : 
#   ┌ Info: SDEProblem with uType SimType{Float64} and tType Float64. In-place: true
#   │ timespan: (0.0, 10.0)
#   └ u0: [1.01, 1.0, 1.0]
#   p = [0.9, 1.0, 1.0, 1.1, 1.0, 1.0, 1.0]
#   du = [0.0, 0.0, 0.0]


#   Erkenntnis:
#   er lässt jetzt irgendwie die ForwardDiff.Dual() Matrixschreibweise weg

#   Wenn man nur 'sol = solve(prob,choosenSolver)' laufen lässt, bekommt man auch
#   keine Matrixschreibweise raus! (in test.jl validiert)

#   """

#   @show predict_fd_sde()  



#   # odeData = solve(remake(prob,p=Flux.data(neuralParameter)),choosenSolver,saveat=t,maxiters = 1e5)
#   # odeData = solve(prob,p=Flux.data(neuralParameter),choosenSolver,saveat=t,maxiters = 1e5)
#   # display only the first ODE in the same figure as the data
#   scatter(t,testSol,color=[1],label = "first ODE data")

#   display(plot!(t,odeData[1,:],ylim=(0,10),label="fit"))

# end

# cb = function()
#   @info "loss function:" loss_fd_sde()
# end 

@info "alles ok vorm Flux"

# NOTE: cb habe ich rausgenommen, da sich sonst die Simulationsanzahl verdoppelt

Flux.train!(loss_fd_sde, [neuralParameter], data, opt)#, cb = cb)

simulationData = predict_fd_sde()

@info "loss function:" loss_fd_sde()
@info "trained parameters:" neuralParameter

# scatter(t,testSol,color=[1],label = "first ODE data")

# display(plot!(t,Tracker.data(simulationData),ylim=(0,10),label="fit"))