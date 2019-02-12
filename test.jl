# # include("/Users/janpiotraschke/GithubRepository/ProjectQ/test.jl")
# # import Pkg; Pkg.add("Flux")
# # import Pkg; Pkg.add("DiffEqFlux")
# # import Pkg; Pkg.add("BSON")
# # Flux is the neural network framework
# Flux finds the parameters of the neural network (p) which minimize the cost function
using Flux, DiffEqFlux, DifferentialEquations, Plots
# using BSON: @save

"""
Next we define a single layer neural network that uses the diffeq_rd layer
function that takes the parameters and returns the solution of the x(t) variable
"""




# # # Setup ODE to optimize
# # function lotka_volterra(du,u,p,t)
# #     x, y = u
# #     α, β, δ, γ = p
# #     du[1] = dx = α*x - β*x*y
# #     du[2] = dy = -δ*y + γ*x*y
# # end

# # u0 = Float32[1.0; 1.0]

# # tspan = (0.0,5.0)
# # p = [1.5,1.0,3.0,1.0]

# # # start:step:stop
# # t = tspan[1]:0.2:tspan[2]

# # problem = ODEProblem(lotka_volterra,u0,tspan,p)

# # @info "start of the simulation"

# # odeData = Array(solve(problem,Tsit5(),saveat=t))

# # @show typeof(odeData)
# # @info "the equation system is solved"

# # # In Flux, we can define a multilayer perceptron with 1 hidden layer and
# # # a tanh activation function like:
# # dudt = Chain(x -> x.^3,
# #              Dense(2,50,tanh),
# #              Dense(50,2))
# # @show dudt

# # # we will wrap our parameters in param to be tracked by Flux
# # ps = Flux.params(dudt)

# # # pTest = param(p)
# # # params = Flux.Params([pTest])

# # # # diffeq_rd takes in parameters p for the integrand, puts it in the differential 
# # # # equation defined by prob, and solves it with the chosen arguments (solver, tolerance, etc)

# # # function predict_rd() # Our 1-layer neural network
# # #   diffeq_rd(pTest,prob,Tsit5(),saveat=0.1)[1,:]
# # # end
# # # @info "ps from Flux:"
# # # @info ps 

# # """
# # Notice that the neural_ode has the same timespan and saveat as the solution 
# # that generated the data. This means that given an x (and initial value), it will 
# # generate a guess for what it thinks the time series will be where the dynamics 
# # (the structure) is predicted by the internal neural network.
# # """

# # n_ode = x->neural_ode(dudt,x,tspan,Tsit5(),saveat=t,reltol=1e-7,abstol=1e-9)

# # # get the prediction using the correct initial condition
# # pred = n_ode(u0) 

# # @info Flux.data(pred)


# # # plot only the first ode (for simplification)
# # scatter(t,odeData[1,:],label="data")
# # scatter!(t,Flux.data(pred[1,:]),label="prediction")

# # # @show Flux.data(pred[1,:])

# # # define a prediciton and loss function for the model training
# # function predict_n_ode()
# #     n_ode(u0)
# # end

# # # loss between our prediction and data
# # loss_n_ode() = sum(abs2,odeData .- predict_n_ode())
# # # loss_fd_sde() = sum(abs2,x-1 for x in predict_fd_sde())

# # # train the neural network
# # data = Iterators.repeated((), 5)
# # opt = ADAM(0.1)
# # cb = function () #callback function to observe training
# #   display(loss_n_ode())
# #   # plot current prediction against data
# #   cur_pred = Flux.data(predict_n_ode())
# #   pl = scatter(t,odeData[1,:],label="data")
# #   scatter!(pl,t,cur_pred[1,:],label="prediction")
# #   display(plot(pl))
# # end

# # # # Display the ODE with the initial parameter values.
# # cb()

# # # # the actual training part
# # # Flux.train!(loss_n_ode, ps, data, opt, cb = cb)




# # # SDE with neural network
# # using Flux, DiffEqFlux, DifferentialEquations, Plots

# # function lotka_volterra(du,u,p,t)
# #   x, y = u
# #   α, β, δ, γ = p
# #   du[1] = dx = α*x - β*x*y
# #   du[2] = dy = -δ*y + γ*x*y
# # end

# # function lotka_volterra_noise(du,u,p,t)
# #   du[1] = 0.1u[1]
# #   du[2] = 0.1u[2]
# # end

# # prob = SDEProblem(lotka_volterra,lotka_volterra_noise,[1.0,1.0],(0.0,10.0))

# # p = param([2.2, 1.0, 2.0, 0.4])
# # params = Flux.Params([p])

# # function predict_fd_sde()
# #   diffeq_fd(p,sol->sol[1,:],101,prob,SOSRI(),saveat=0.1)
# # end
# # loss_fd_sde() = sum(abs2,x-1 for x in predict_fd_sde())

# # data = Iterators.repeated((), 5)
# # opt = ADAM(0.1)
# # cb = function ()
# #   display(loss_fd_sde())
# #   display(plot(solve(remake(prob,p=Flux.data(p)),SOSRI(),saveat=0.1),ylim=(0,8)))
# # end

# # # Display the ODE with the current parameter values.
# # cb()

# # Flux.train!(loss_fd_sde, params, data, opt, cb = cb)














# using Flux, DiffEqFlux, DifferentialEquations, Plots

# # TEMP : data generation
# function lotka_volterra_experimental(du,u,p,t)
#     x, y = u
#     α, β, δ, γ = p
#     du[1] = dx = α*x - β*x*y
#     du[2] = dy = -δ*y + γ*x*y
# end

# u00 = Float32[1.0; 1.0]

# tspan0 = (0.0,10.0)
# p0 = [2.5,1.0,3.0,1.0]

# # start:step:stop
# t0 = tspan0[1]:0.2:tspan0[2]

# problem0 = ODEProblem(lotka_volterra_experimental,u00,tspan0,p0)

# @info "start of the simulation"

# experimentalData = Array(solve(problem0,Tsit5(),saveat=t0))

# @info experimentalData

# scatter(t0,experimentalData[1,:],label="experimental data")

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

function lotka_volterra(du,u,p,t)
  x, y = u
  α, β, δ, γ = p
  du[1] = dx = α*x - β*x*y
  du[2] = dy = -δ*y + γ*x*y
end

u0 = [1.01,1.0]
tspan = (0.0,10.0)
p = [1.5,1.0,3.0,1.0]
prob = ODEProblem(lotka_volterra,u0,tspan,p)

# start:step:stop
t = tspan[1]:0.2:tspan[2]

# Generate data from the ODE
# saveat: Denotes specific times to save the solution at
sol = solve(prob,Tsit5(),saveat=t)
A = sol[1,:]
display(plot(t,A,label="first ODE data"))

@info "initial simulation is plotted"


"""Initial Parameter Vector 

which will be changed by the training algorithm.
The param function converts a normal Julia array into a new object that, while 
behaving like an array, tracks extra information that allows us to calculate derivatives
"""
neuralParameter = param(p)

"""
next we define a single layer neural network that uses the diffeq_rd layer 
function that takes the parameters and returns the solution of the x(t) 
variable
"""
function predict_rd() 
  diffeq_rd(neuralParameter,prob,Tsit5(),saveat=t)[1,:]
end

# calculate the sum of the absolute squares of the entries of a vector v: sum(abs2,v)
loss_rd() = sum(abs2,x-1 for x in predict_rd()) # loss function

# Optimize the parameters so the ODE's solution stays near 1
# run 100 iteration 
data = Iterators.repeated((), 5)

# Now we tell Flux to train the neural network by running a 100 epoch to minimise our loss function 
# Optimiser: Descent, Momentum, Nesterov, ADAM
opt = ADAM(0.1)

# # callback function to observe training
cb = function() 
  # using `remake` to re-create our `prob` with current parameters `p`
  odeData = solve(remake(prob,p=Flux.data(neuralParameter)),Tsit5(),saveat=t)

  # display only the first ODE in the same figure as the data
  display(plot(t,odeData[1,:],ylim=(0,10)))
end

# Display the ODE with the initial parameter values.
cb()
Flux.train!(loss_rd, [neuralParameter], data, opt, cb = cb)

# You may wish to save models so that they can be loaded and run in a later 
# session. The easiest way to do this is via BSON.jl.
# @save "mymodel.bson" neuralParameter

# @info "loss function: " loss_rd()