volume_parameter = {
                    'd' : [0.115,'um','cell wall thickness'],
                    'phi' : [1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility', 'fitted Altenburg 2018'],
                    'pi_c' : [2e5, 'Pa', 'critical turgor pressure'],
                    'Lp' : [1.19e-6, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'],
                    'nu' : [0.5, 'dimensionless', 'Poissons ratio'],
                    'k_uptake' : [2e-16, 'mmol s^{-1} um^{-2}'],
                    'k_consumption' : [2.5e-16, 'mmol s^{-1} um^{-3}'],
                    'E_3D' : [2.58e6, 'Pa', 'measured Youngs modulus', 'Goldenbogen & Giese et al. 2016'],
                    'c_e' : [240, 'mM'],
                    'pi_e' : [604594.08, 'mM'],
                    'E': [3440000.0,'Pa'],

                    'T' : [303.15, 'K'],
                    'R' : [8.314, 'J K^-1 mol^-1'],
                    'F' : [96485, 'C mol^-1'],
                    }

# activates all keys as variables with the values in the list
for key,value in volume_parameter.items():
    exec(key + '=value[0]')

modulus_adjustment = (1 - nu ** 2) ** (-1)  # dimensionless
E = modulus_adjustment * E_3D  # adjusted to 2D Young's modulus (surface)
print(E)
volume_init_values = {
                    'r_os' : [1.18773900649, 'r_os', 'um'],
                    'r_b' : [0.496161324363, 'r_b', 'um'],
                    'r' : [1.68390033085, 'r', 'um'],
                    'pi_t' : [2e5, 'pi_t', 'Pa','turgor pressure'],
                    'R_ref' : [1.36108685239, 'R_ref', 'um'],
                    'c_i' : [6.38904517734e-12, 'c_i', 'mmol','internal concentration of osmolytes']
                    }
