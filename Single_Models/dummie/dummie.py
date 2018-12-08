import numpy as np
from collections import OrderedDict

dummie_parameter = {
                    'b' : [0.25, 'dimensionless'],
                    'c' : [5.0, 'dimensionless']
                    }

for key,value in dummie_parameter.items():
    exec(key + '=value[0]')

dummie_init_values = {
                    'theta' : [np.pi - 0.1, 'theta','dimensionless'],
                    'omega' : [0.0, 'omega','dimensionless']
                    }

# dictionary sorted by key
#ordered = OrderedDict(sorted(dummie_parameter.items(), key=lambda t:t[0]))
#print(type(ordered))
