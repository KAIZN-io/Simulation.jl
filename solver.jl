"""copy paste this code into the terminal"""

# include("/Users/janpiotraschke/GithubRepository/ProjectQ/solver.jl")
# import Pkg; Pkg.add("DifferentialEquations")
# import Pkg; Pkg.add("Plots")
# import Pkg; Pkg.add("ParameterizedFunctions")
# import Pkg; Pkg.add("BenchmarkTools")
# import Pkg; Pkg.add("SymPy")

using ParameterizedFunctions
using DifferentialEquations, BenchmarkTools
using Plots; plotly()
using SymPy

# define the equation as a string; maybe with the help of Sympy
myString = "4 * x - y"

# parse the string and make it an expression
ex = Meta.parse(myString)

# defining our ODE system as parameterized functions
f_lorenz = @ode_def_bare LorenzSDE begin
  dx = σ*(y-x) * eval(ex)
  dy = x*(ρ-z) - y
  dz = x*y - β*z
end σ ρ β

# defining our noise as parameterized functions
noiseModelSystem(du,u,p,t) = @.(du = 3.0)

# define the initial Values --> [1*m] vector 
initialValues=[1.0;1.0;1.0]

# define the parameters --> [m * n] matrix
parameter=[10.0,28.0,8/3]

# time array (must be a tuple)
timeRange = (0.0,2.0)

# # change the Gaussian white noise
# choosenNoise = WienerProcess(0.0,0.0,0.0)

# define the Problem  -->  Gaussian white noise is default
# set the seed for reproducing the same stochastic simulation
problem = SDEProblem(f_lorenz, noiseModelSystem, initialValues, timeRange, parameter, seed=1234)#, noise=choosenNoise)

# solve the problem
sol = solve(problem)

# check how long it takes to solve the equation system 
# @benchmark sol = solve(problem)#, save_everystep=false)


# plot the solution
plot(sol, linewidth=3,title="Solution of the SDE system")

# # 3d plot
# plot(sol,vars=(1,2,3))

