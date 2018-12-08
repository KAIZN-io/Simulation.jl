ion_parameter = {
                'ATP_stimulus' : [2.5, 'mM'],

                # NOTE: original ion parameter values
                # 'V_out' : [2.85e-6,'m^3'],
                # 'V_in' : [1.8 * 1e-11,'m^3'],
                # 'Surf' : [2.29e-5, 'm^2'],

                # NOTE: from the combined_models
                'V_out' : [28.95 * 1e-15,'m^3'],
                'V_in' : [58 * 1e-18,'m^3'],
                'Surf' : [72.38 * 1e-12, 'm^2'],

                'pbc' : [200,'mM pH^-1'],
                'C_m' : [1e-2, 'xxxxxxx'],
                'c_strich_ATP' : [0.316, 'mM'],
                'K_eq' : [1e-6, 'dimensionless'],

                'L_HHaG' : [0.0019 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ArHaG' : [-0.00195, 'mol^2 J^-1 m^-2 s^-1'],
                'L_HNa' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaH' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                'L_KK' : [6.37 * 1e-11, 'mol^2 J^-1 m^-2 s^-1'],
                'L_HCl' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClH' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaNa' : [3.03 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClCl' : [1.04 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                'L_HK' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],
                'L_KH' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],

                'k_incrHH' : [3.54 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_incrArH' : [-3.64 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_ATPincr' : [10, 'mol m^-3 s^-1'],

                'T' : [303.15, 'K'],
                'R' : [8.314, 'J K^-1 mol^-1'],
                'F' : [96485, 'C mol^-1'],
                }


# activates all keys as variables with the values in the list
for key,value in ion_parameter.items():
    exec(key + '=value[0]')

k_ATPdecr = k_ATPincr / ATP_stimulus
k_decrArH =  k_incrArH / L_ArHaG
k_decrHH = k_incrHH / L_HHaG

ion_init_values = {
                'H_in' : [3.063e-3  , 'H_in', 'mM','original/ion_model'],
                'K_in' : [75.54 , 'K_in', 'mM','original/ion_model'],
                'Cl_in' : [0.545 ,'Cl_in' , 'mM','original/ion_model'],
                'Na_in' : [29.98 , 'Na_in', 'mM','original/ion_model'],

                # NOTE: Werte vom originalen Ion-Modell
                # 'H_out' : [3.162e-3, 'H_out', 'mM'],
                # 'K_out' : [0.1, 'K_out', 'mM'],
                # 'Cl_out' : [0.1, 'Cl_out', 'mM'],
                # 'Na_out' : [0.01, 'Na_out', 'mM'],

                # NOTE: Werte vom combined_models
                'H_out' : [(3.162e-3)* 1126 , 'H_out', 'mM','original/ion_model'],
                'K_out' : [0.1 * 1126, 'K_out', 'mM','original/ion_model'],
                'Cl_out' : [0.1 * 1126, 'Cl_out', 'mM','original/ion_model'],
                'Na_out' : [0.01 * 1126 , 'Na_out', 'mM','original/ion_model'],

                ######
                'ATP' : [2.477, 'ATP', 'mM'],
                'Deltaphi' : [-0.168, 'Deltaphi', 'V'],

                # changeable coefficients, init for time = 0 min
                'L_ArH' : [0, 'L_ArH', '... s^-1'],
                'L_HH' : [1.62 * 1e-9, 'L_HH', '... s^-1']
                }
