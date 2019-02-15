# include("/Users/janpiotraschke/GithubRepository/ProjectQ/test.jl")
# import Pkg; Pkg.add("Flux")
# import Pkg; Pkg.add("DiffEqFlux")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("BSON")

# Flux is the neural network framework
# Flux finds the parameters of the neural network (p) which minimize the cost function
using Flux, DiffEqFlux, DifferentialEquations, Plots
# using BSON: @save

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

# SDE with neural network
function lotka_volterra(du,u,p,t)
  x, y = u
  α, β, δ, γ = p
  du[1] = dx = α*x - β*x*y
  du[2] = dy = -δ*y + γ*x*y
end

# defining our noise as parameterized functions
noiseModelSystem(du,u,p,t) = @.(du = 3.0)

function lotka_volterra_noise(du,u,p,t)
  du[1] = 0.1u[1]
  du[2] = 0.1u[2]
end

u0 = [1.01,1.0]
tspan = (0.0,10.0)
p = [1.5,1.0,3.0,1.0]

# choose a solver: SOSRI(), Tsit5()
choosenSolver = SOSRI()

# start:step:stop
t = tspan[1]:0.2:tspan[2]

prob = SDEProblem(lotka_volterra,lotka_volterra_noise,u0, tspan, p)#,seed=1234)



"""Initial Parameter Vector 

which will be changed by the training algorithm.

The param function converts a normal Julia array into a new object that, while 
behaving like an array, tracks extra information that allows us to calculate 
derivatives
"""
neuralParameter = param([2.2, 1.0, 2.0, 0.4])


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
data = Iterators.repeated((), 100)

opt = ADAM(0.1)

# callback function to observe training
cb = function ()
  @show loss_fd_sde()

  """ Infos about the solver

  returns = n-element Array{Array{Float64,1},1}
  saveat: Denotes specific times to save the solution at
  maxiters: Maximum number of iterations before stopping. Defaults to 1e5.
  """
  # using `remake` to re-create our `prob` with current parameters `p`
  odeData = solve(remake(prob,p=Flux.data(neuralParameter)),choosenSolver,saveat=t,maxiters = 1e5)

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

Flux.train!(loss_fd_sde, [neuralParameter], data, opt, cb = cb)


@info "trained parameters:" neuralParameter


# # # You may wish to save models so that they can be loaded and run in a later 
# # # session. The easiest way to do this is via BSON.jl.
# # # @save "mymodel.bson" neuralParameter
