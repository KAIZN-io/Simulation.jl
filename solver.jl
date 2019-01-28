"""copy paste this code into the terminal"""
# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")

using DifferentialEquations
using Plots; plotly()

# defining our ODE system 
# function lorenz(du,u,p,t)
#  du[1] = p[1]*(u[2]-u[1])
#  du[2] = u[1]*(p[2]-u[3]) - u[2]
#  du[3] = u[1]*u[2] - p[3]*u[3]
# end
function lorenz(du,u,p,t)
 du[1] = 10.0*(u[2]-u[1])
 du[2] = u[1]*(28.0-u[3]) - u[2]
 du[3] = u[1]*u[2] - (8/3)*u[3]
end

α=1
β=1

# define the initial Values 
initialValues=[1.0;0.0;0.0]

# define the parameters
p=[10.0,28.0,8/3]


f(u,p,t) = α*u
g(u,p,t) = β*u
dt = 1//2^(4)

# time array (must be a tuple)
timeRange = (0.0,2.0)

# SDEProblem(function, noise, initial values, time range)
# prob = SDEProblem(f,g,initialValues,timeRange)

# define the Problem --> it is now a ODEProblem
problem = ODEProblem(lorenz, initialValues, timeRange)

# solve the problem
sol = solve(problem,EM(),dt=dt)

# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")
