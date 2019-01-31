"""copy paste this code into the terminal"""

# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("ParameterizedFunctions")
# import Pkg; Pkg.add("BenchmarkTools")
# import Pkg; Pkg.add("Logging")

using ParameterizedFunctions
using DifferentialEquations, BenchmarkTools
using Plots; plotly()
using Logging

# get the parameter for the model
myParameterList = ["σ=10.0", "ρ=28.0", "β=8/3"]

# make the parameter global 
for i = 1:size(myParameterList)[1]
    ex = Meta.parse(myParameterList[i])
    eval(ex)
end

function getMaxTermCount(arrayTerms)
  maxTermCount = 0
  for row in eachindex(arrayTerms)
    y = arrayTerms[row]
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

# matrix with the variables name
# variableMatrix = ["e"; "d"]
variableMatrix = ["e"; "d"; "dx"; "dy"; "dz"]
# variableMatrix = ["e"; "d"; "du[1]"; "du[2]"; "du[3]"]




# get the len of the array
myArraySize = size(variableMatrix)[1]

# array of arrays 
# inputTermArray = Array[["+3*x", "-2*y"], ["+4*y", "-x"]]
inputTermArray = Array[["+3*x", "-2*y"], ["+4*y", "-x"], ["+σ*y", "-σ*x"], ["+x*ρ" ,"-x*z" ,"- y"], ["+x*y" ,"- β*z"]]

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

# re-unit the variable matrix with their terms and precompile the equations
expressionMatrix = [Meta.parse(string(variableMatrix[i], "=" ,activatedTermMatrix[i])) for i in 1:myArraySize]

@info "expression matrix for terms is created successfully"

function evalExpressionForSolver(u,du)
  global x,y,z = u
  global dx,dy,dz = du

  for j = 1:myArraySize
    eval(expressionMatrix[j])

    # if last equation is calculated --> overgive the solution the solver 
    if j == myArraySize
      global duDummie = [dx, dy, dz]
    end
  end
  du[1], du[2], du[3] = duDummie
  return du[1], du[2], du[3]

end


function parameterized_lorenz(du,u,p,t)
  evalExpressionForSolver(u,du)

  # global x,y,z = u
  # global dx,dy,dz = du

  # for j = 1:myArraySize
  #   eval(expressionMatrix[j])

  #   # if last equation is calculated --> overgive the solution the solver 
  #   if j == myArraySize
  #     global duDummie = [dx, dy, dz]
  #   end
  # end

  # du[1], du[2], du[3] = duDummie

end

# f_lorenz = @ode_def_bare LorenzSDE begin
#   for j = 1:myArraySize
#     eval(expressionMatrix[j])
#   end
#   # println(dx,dy,dz)
#   dx = σ*(y-x) * e
#   dy = x*(ρ-z) - y *d 
#   dz = x*y - β*z
# end 

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

problem = SDEProblem(parameterized_lorenz, noiseModelSystem, initialValues, timeRange, seed=1234)#, noise=choosenNoise)

@info "start the simulation"
# solve the problem
sol = solve(problem)

@info "the equation system is solved"

# # check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)#, save_everystep=false)

# # plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")

# # 3d plot
# plot(sol,vars=(1,2,3))