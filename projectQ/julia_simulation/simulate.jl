using Pkg

Pkg.add("Flux")
Pkg.add("DiffEqFlux")
Pkg.add("DifferentialEquations")
Pkg.add("Plots")
Pkg.add("Logging")
Pkg.add("Documenter")

using Flux, DiffEqFlux, DifferentialEquations, Plots, Logging
using Flux.Tracker


mutable struct SimType{T} <: DEDataVector{T}
    x::Array{T,1}
    f1::T
end


function getMaxTermCount(arrayTerms)
    maxTermCount = 0
    for row in eachindex(arrayTerms)
        arraySize = length(arrayTerms[row])
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

function evalExpressionForSolver(u,du,placeHolder)

    # evaluate the initial values
    for i = 1:length(u)
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

    # how long the vector is
    sizeA = length(rawValuesForNN)

    # how long the vector should be
    B = resize!(A, sizeA)

    # reshape the matrix
    NNMatrix = reshape(B, length(odeNames), maxTermCount)

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

    return du
end

# define the noise
noiseModelSystem(du,u,p,t) = @.(du = 0.01)



# callbacks
function condition(u,t,integrator)
    t in tstop
end

function affect!(integrator)
    # add the term to the ode
    integrator.u[1] += stimulus

end

function simulate(model, parameter, initialValues, stimuli, start, stop, stepSize)

    # get the parameter for the model
    myParameterList = map((key)->string(key,"=",parameter[key]),collect(keys(parameter)))

    # array with the algebraic keys
    keysAlgebraic = collect(keys(model["algebraic"]))

    # array with the ODEs
    odeNames = collect(keys(model["differential"]))

    variableMatrix = [keysAlgebraic; odeNames]

    # array of arrays
    odeMatrix = map((var)->model["differential"][var],odeNames)
    algebraicMatrix = map((var)->model["algebraic"][var],keysAlgebraic)

    inputTermArray = [algebraicMatrix; odeMatrix]

    odeVariable = collect(keys(initialValues))

    # define the initial Values --> [n*1] vector
    initialValuesList = map((var)->initialValues[var],odeVariable)

    initialValues = SimType(initialValuesList, 0.0)

    # time array (must be a tuple)
    timeRange = (start, stop)

    # start:step:stop
    t = timeRange[1]:stepSize:timeRange[2]

    # impuls events
    tstop = map((stimulus)->stimulus["time"],stimuli)

    # apply a stimulus value
    stimulus = 5.5


    # choose a solver: SOSRI(), Tsit5()
    choosenSolver = SOSRI()

    # run n iteration
    nIteration = 3

    timePoints = sort(append!(collect(t),tstop))

    # make the unmutable parameter global
    for i = 1:length(myParameterList)
        ex = Meta.parse(myParameterList[i])
        eval(ex)
    end

    # preparation --> assign the equations to a dict
    equationDict = Dict()
    for i = 1:length(variableMatrix)
        equationDict[variableMatrix[i]] = inputTermArray[i]
    end




    # get the len of the array
    myArraySize = length(variableMatrix)

    # get the maximal term count
    maxTermCount = getMaxTermCount(inputTermArray)

    # create the generel term matrix
    emptyTermMatrix = fill("", myArraySize, maxTermCount)
    emptyOdeMatrix = fill("", length(odeNames), maxTermCount)

    # fill the term matrix with the terms
    termMatrix = fillTermMatrix(emptyTermMatrix,inputTermArray)
    realOdeMatrix = fillTermMatrix(emptyOdeMatrix,odeMatrix)

    # create the neuronal network matrix filled with ones
    neuronalNetworkMatrix = ones(length(odeNames),maxTermCount)

    # create the parameters of the neural network --> copy the array dimensions
    neuronalNetworkMatrixVariable = similar(neuronalNetworkMatrix, String)

    # fill the neuronalNetworkMatrixVariable with the parameters
    for row in 1:length(odeNames)
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
    for i in 1:length(rawValuesForNN)
        if rawValuesForNN[i] == 1
            append!(valuesForNN,rawValuesForNN[i])
            push!(variablesForNN,rawVariablesForNN[i])
        end
    end



    cb = DiscreteCallback(condition, affect!)

    # could be a set of callback
    cbs = CallbackSet(cb)

    # change the Gaussian white noise
    choosenNoise = WienerProcess(0.0,0.0,0.0)

    # define the Problem
    prob = SDEProblem((du,u,p,t)->evalExpressionForSolver(u,du,p), noiseModelSystem, initialValues, timeRange, valuesForNN, seed=1234)#, noise=choosenNoise)

    """Initial Parameter Vector
    which will be changed by the training algorithm.
    """

    neuralParameter = param(valuesForNN)


    """
    Next we define a single layer neural network that uses the diffeq_rd (for ODE)
    or a diffeq_fd (for SDE) layer function that takes the parameters and
    returns the solution of the x(t) variable
    """

    """ Infos about the solver

    returns = n-element Array{Array{Float64,1},1}
    saveat: Denotes specific times to save the solution at
    maxiters: Maximum number of iterations before stopping. Defaults to 1e5.
    """

    function predict_fd_sde()

        diffeq_fd(neuralParameter,sol->sol[1:length(odeNames),:],(length(t)+length(tstop))*length(odeNames),prob,choosenSolver,saveat=t,callback = cbs, tstops=tstop)

    end


    simulationData = predict_fd_sde()
    odeData = Tracker.data(simulationData)

    # sort the time-series per substance in the following matrix
    simulationDataMatrix = zeros(length(timePoints),length(odeNames)+1)

    # append time points to matrix
    simulationDataMatrix[:,1] += timePoints

    for j in 1:length(odeNames)
        iterNum = 1
        for i in j:3:length(odeData)

            simulationDataMatrix[iterNum,j+1] = odeData[i]
            iterNum +=1

        end
    end
end


