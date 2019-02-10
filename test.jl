# include("/Users/janpiotraschke/GithubRepository/ProjectQ/test.jl")
# import Pkg; Pkg.add("Flux")
# import Pkg; Pkg.add("DiffEqFlux")

# # Flux is the neural network framework
# Flux finds the parameters of the neural network (p) which minimize the cost function

using Flux, DiffEqFlux, DifferentialEquations, Plots

u0 = Float32[2.; 0.]
datasize = 30
tspan = (0.0f0,1.5f0)

function trueODEfunc(du,u,p,t)
    true_A = [-0.1 2.0; -2.0 -0.1]
    du .= ((u.^3)'true_A)'
end
t = range(tspan[1],tspan[2],length=datasize)
prob = ODEProblem(trueODEfunc,u0,tspan)
ode_data = Array(solve(prob,Tsit5(),saveat=t))

dudt = Chain(x -> x.^3,
             Dense(2,50,tanh),
             Dense(50,2))
ps = Flux.params(dudt)
n_ode = x->neural_ode(dudt,x,tspan,Tsit5(),saveat=t,reltol=1e-7,abstol=1e-9)

pred = n_ode(u0) # Get the prediction using the correct initial condition
scatter(t,ode_data[1,:],label="data")
scatter!(t,Flux.data(pred[1,:]),label="prediction")

function predict_n_ode()
  n_ode(u0)
end
loss_n_ode() = sum(abs2,ode_data .- predict_n_ode())

data = Iterators.repeated((), 5)
opt = ADAM(0.1)
cb = function () #callback function to observe training
  display(loss_n_ode())
  # plot current prediction against data
  cur_pred = Flux.data(predict_n_ode())
  pl = scatter(t,ode_data[1,:],label="data")
  scatter!(pl,t,cur_pred[1,:],label="prediction")
  display(plot(pl))
end

# Display the ODE with the initial parameter values.
cb()

Flux.train!(loss_n_ode, ps, data, opt, cb = cb)




# SDE with neural network
# using Flux, DiffEqFlux, DifferentialEquations, Plots

# function lotka_volterra(du,u,p,t)
#   x, y = u
#   α, β, δ, γ = p
#   du[1] = dx = α*x - β*x*y
#   du[2] = dy = -δ*y + γ*x*y
# end

# function lotka_volterra_noise(du,u,p,t)
#   du[1] = 0.1u[1]
#   du[2] = 0.1u[2]
# end

# prob = SDEProblem(lotka_volterra,lotka_volterra_noise,[1.0,1.0],(0.0,10.0))

# p = param([2.2, 1.0, 2.0, 0.4])
# params = Flux.Params([p])

# function predict_fd_sde()
#   diffeq_fd(p,sol->sol[1,:],101,prob,SOSRI(),saveat=0.1)
# end
# loss_fd_sde() = sum(abs2,x-1 for x in predict_fd_sde())

# data = Iterators.repeated((), 5)
# opt = ADAM(0.1)
# cb = function ()
#   display(loss_fd_sde())
# #   display(plot(solve(remake(prob,p=Flux.data(p)),SOSRI(),saveat=0.1),ylim=(0,8)))
# end

# # Display the ODE with the current parameter values.
# cb()

# Flux.train!(loss_fd_sde, params, data, opt, cb = cb)














# using Flux, DiffEqFlux, DifferentialEquations, Plots

# ## Setup ODE to optimize
# function lotka_volterra(du,u,p,t)
#   x, y = u
#   α, β, δ, γ = p
#   du[1] = dx = α*x - β*x*y
#   du[2] = dy = -δ*y + γ*x*y
# end

# u0 = [1.0,1.0]
# tspan = (0.0,10.0)
# p = [1.5,1.0,3.0,1.0]
# prob = ODEProblem(lotka_volterra,u0,tspan,p)


# # Generate data from the ODE
# sol = solve(prob,Tsit5(),saveat=0.1)
# A = sol[1,:] # length 101 vector

# plot(sol)
# # start:step:stop
# t = 0:0.1:10.0
# scatter!(t,A)

# # Build a neural network that sets the cost as the difference from the
# # generated data and 1

# p = param([2.2, 1.0, 2.0, 0.4]) # Initial Parameter Vector

# # diffeq_rd takes in parameters p for the integrand, puts it in the differential 
# # equation defined by prob, and solves it with the chosen arguments (solver, tolerance, etc)

# function predict_rd() # Our 1-layer neural network
#   diffeq_rd(p,prob,Tsit5(),saveat=0.1)[1,:]
# end

# loss_rd() = sum(abs2,x-1 for x in predict_rd()) # loss function

# # Optimize the parameters so the ODE's solution stays near 1
# # run 100 epoch 
# data = Iterators.repeated((), 5)

# # Now we tell Flux to train the neural network by running a 100 epoch to minimise our loss function 
# opt = ADAM(0.1)
# cb = function () #callback function to observe training
#   display(loss_rd())
#   # using `remake` to re-create our `prob` with current parameters `p`
#   display(plot(solve(remake(prob,p=Flux.data(p)),Tsit5(),saveat=0.1),ylim=(0,6)))
# end

# # Display the ODE with the initial parameter values.
# cb()

# Flux.train!(loss_rd, [p], data, opt, cb = cb)
