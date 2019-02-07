def (wantedCI)

# start simulation
# call Julia x times and get the simulation results
simulationResults = Julia(iterationNumber = x, Model)

# calculate the mean for each substance / column
meanList

# calculate the corresponding variance
varianceList 

# calculate CI list / the error estimation , t-Faktor für 95,4 % Sicherheit
# CI = f(LCV) oder f(GCV)
t = 4.30
CI = []
for i in variance:
    CI.append("{0:.2f}".format(t*np.sqrt(i/n)))

# check the break rule condition
if all CI in list >= wantedCI:
    break function

