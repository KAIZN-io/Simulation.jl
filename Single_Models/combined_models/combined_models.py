combined_models_parameter = {
                'T' : [303.15, 'K'],
                'R' : [8.314, 'J K^-1 mol^-1'],
                'F' : [96485, 'C mol^-1'],

                'k_phoPbs2' : [39.22 /60, 's^-1'],
                'k_dephoPbs2' : [ 13.44 /60,'s^-1'],
                'k_phoHog1' : [11.2 * 1e3 /60 ,'mM^-1 s^-1'],

                'k_dephoHog1PPn' : [ 4.144 /60 ,'s^-1'],
                'k_dephoHog1PPc' : [0.09061/60 ,'s^-1'],
                'k_impHog1PPc' : [1.195/60 ,'s^-1'],
                'k_s0Glyc' : [ 5248 * 1e-3/60,'mM s^-1'],
                'k_s1Glyc' : [ 56140 * 1e-3/60,'mM s^-1'],
                'k_s2Glyc' : [1139/60 ,'s^-1'],
                'k_tYt' : [ 0.008934 /60,'s^-1'],
                'k_impHog1c' : [ 0.7528 /60,'s^-1'],
                'k_expHog1PPn' : [7.076 /60 ,'s^-1'],
                'k_exp0Glyc' : [0.005/60 ,'s^-1'],
                'k_s0Yt' : [0.01211 * 1e-3 /60 ,'mM s^-1'],
                'k_exp1Glyc' : [0.02963 /60 ,'s^-1'],
                'k_s1Yt' : [1.204 /60 ,'s^-1'],
                'k_expHog1n' : [6.36/60 ,'s^-1'],
                'PI_t0' : [ 0.875 * 1e6,'Pa', 'turgor pressure/unstressed'],
                'PI_i0' : [ 1.5 * 1e6,'Pa', 'internal osmotic pressure/unstressed'],
                'PI_e0' : [0.625 * 1e6 ,'Pa', 'external osmotic pressure/unstressed'],
                'Glyc_ex' : [0 ,'mM', 'eine Konstante hier'],

                # NOTE: G is now an algebraic equation
                #'G' : [72.4607 ,'um^2'],
                'w' : [ 4.688 * 1e-3 * 1e6,'J m^-3 mM^-1'],
                #'Lp' : [0.2497 / 60 * 1e-6 ,'um Pa^-1 s^-1'],
                'f_V_cyt' : [0.5 ,'dimensionless'],
                'n_Hog1_total' : [6780 ,'xxx', 'total number of Hog1'],
                'V_osPIt' : [30.63 ,'fL'],
                'V_os0' : [34.8 ,'fL', 'volume before osmotic change'],
                'V_b' : [ 23.2,'fL','fixed part of the cell volume'],
                'alpha' : [0.18 * 1e6 ,'Pa'],   #orginal: [0.398 * 1e6 ,'Pa']
                'beta' : [ 0.6,'dimensionless'],  #original: [ 0.2992,'dimensionless']
                'gamma' : [0.18 *1e6 ,'Pa'], #original: [0.9626 *1e6 ,'Pa']
                'tau' : [20 * 60 ,'s'],
                'n_0' : [4.176 * 1e3 ,'mmol'],
                'hill_exponent' : [8,'dimensionless'],
                'hill_exponent_eflux' : [12,'dimensionless'],

                # from volume model
                'd' : [0.115,'um','cell wall thickness'],
                'phi' : [1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility', 'fitted Altenburg 2018'],
                'pi_c' : [2e5, 'Pa', 'critical turgor pressure'],
                #'Lp': [0, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'],
                'Lp' : [1.19e-6, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'],
                'nu' : [0.5, 'dimensionless', 'Poissons ratio'],
                'k_uptake' : [2e-16, 'mmol s^{-1} um^{-2}'],
                'k_consumption' : [2.5e-16, 'mmol s^{-1} um^{-3}'],
                'E_3D' : [2.58e6, 'Pa', 'measured Youngs modulus', 'Goldenbogen & Giese et al. 2016'],

                # from ion model
                'ATP_stimulus' : [2.5, 'mM'],

                #'V_out' : [2.85e-6,'m^3'],

                # umgerechnetes Volumen für kombiniertes Hog Model
                #'V_out' : [2.85 * 1e12,'fL'],
                # neu definierte externe Umgebung--> Experiment naeher
                'V_out' : [28.95 * 1e3, 'fL'],

                #'Surf' : [2.29e-5, 'm^2'],
                'pbc' : [200,'mM pH^-1'],
                'C_m' : [1e-2, 'xxxxxxx'],
                'c_strich_ATP' : [0.316, 'mM'],
                'K_eq' : [1e-6, 'dimensionless'],

                # TODO: change the unit of L_XX
                'L_HHaG' : [0.0019  , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ArHaG' : [-0.00195 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HNa' : [-6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaH' : [-6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_KK' : [6.37 * 1e-11 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HCl' : [1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClH' : [1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_NaNa' : [3.03 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_ClCl' : [1.04 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_HK' : [-2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'],
                'L_KH' : [-2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'],

                #'L_HHaG' : [0.0019, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ArHaG' : [-0.00195, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HNa' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_NaH' : [-6.31 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_KK' : [6.37 * 1e-11, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HCl' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ClH' : [1.298 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_NaNa' : [3.03 * 1e-15, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_ClCl' : [1.04 * 1e-9, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_HK' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],
                #'L_KH' : [-2.072097044 * 1e-16, 'mol^2 J^-1 m^-2 s^-1'],
                #####
                'k_incrHH' : [3.54 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_incrArH' : [-3.64 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'],
                'k_ATPincr' : [10, 'mol m^-3 s^-1'],

                'c_ext_extra' : [0,'mM']
                }

for key,value in combined_models_parameter.items():
    exec(key + '=value[0]')

modulus_adjustment = (1 - nu ** 2) ** (-1)  # dimensionless
E = modulus_adjustment * E_3D  # adjusted to 2D Young's modulus (surface)

k_ATPdecr = k_ATPincr / ATP_stimulus
k_decrArH =  k_incrArH / L_ArHaG
k_decrHH = k_incrHH / L_HHaG

combined_models_init_values = {
                'Pbs2' : [0.1231 * 1e-3, 'Pbs2', 'mM', 'original/hog_model'],              # unphosphorylated Pbs2
                'Pbs2PP' : [0.000616 * 1e-3, 'Pbs2PP', 'mM', 'original/hog_model'],            # phosphorylated Pbs2
                'Hog1c' : [0.3426 * 1e-3, 'Hog1c', 'mM', 'original/hog_model'],            # unphosphorylated cytoplasmic Hog1
                'Hog1PPc' : [0.004443 * 1e-3, 'Hog1PPc', 'mM', 'original/hog_model'],        # phosphorylated cytoplasmic Hog1
                'Hog1n' : [0.2918 * 1e-3, 'Hog1n', 'mM', 'original/hog_model'],              # unphosphorylated nuclear Hog1
                'Hog1PPn' : [0.00338 * 1e-3, 'Hog1PPn', 'mM', 'original/hog_model'],          # phosphorylated nuclear Hog1
                'Glyc_in' : [57600 * 1e-3, 'Glyc_in', 'mM', 'original/hog_model'],            # intracellular glycerol

                # Yt is the time delay for the expression of glycerol-producing proteins
                'Yt' : [1.811 * 1e-3, 'Yt', 'mM', 'original/hog_model'],

                'z1' : [0.00338 * 1e-3, 'z1', 'mM', 'original/hog_model'],              # z = delay of transcriptional feedback on glycerol production
                'z2' : [0.00338 * 1e-3, 'z2', 'mM', 'original/hog_model'],
                'z3' : [0.00338 * 1e-3, 'z3', 'mM', 'original/hog_model'],
                'z4' : [0.00338 * 1e-3, 'z4', 'mM', 'original/hog_model'],

                'r_os' : [1.819281, 'r_os', 'um', 'simulated/volume_model for V=58fl'],
                'r_b' : [0.580719, 'r_b', 'um', 'simulated/volume_model for V=58fl'],
                'r' : [2.4, 'r', 'um', 'simulated/volume_model for V=58fl'],
                'R_ref' : [1.783877, 'R_ref', 'um', 'simulated/volume_model for V=58fl'],

                #V_cell = [4/3 * np.pi * r[0]**3, 'V_cell', 'fL', 'calculated/volume_model']

                # NOTE: the volume of the initial V_os is now calculated --> V_os = 57 fL
                #V_os = [4/3 * np.pi * r[0]**3 - 4/3*np.pi*r_b[0]**3,\
                #        'V_os', 'fL', 'osmotic volume of the cell', 'calculated/volume_model']

                #V_cell = [58, 'V_cell', 'fL', 'original/hog_model']
                #V_os = [34.8, 'V_os', 'fL', 'osmotic volume of the cell', 'original/hog_model']

                #r_os = [1.18773900649, 'r_os', 'um', 'original/volume_model']
                #r_b = [0.496161324363, 'r_b', 'um', 'original/volume_model']
                #r = [1.68390033085, 'r', 'um', 'original/volume_model']
                #R_ref = [1.36108685239, 'R_ref', 'um', 'original/volume_model']

                'pi_t' : [2e5, 'pi_t', 'Pa','turgor pressure','original/volume_model'],

                # * 1.95 Faktor wegen Normierung auf c_i = 320 mM
                'H_in' : [3.063e-3  , 'H_in', 'mM','original/ion_model'],
                'K_in' : [75.54 , 'K_in', 'mM','original/ion_model'],
                'Cl_in' : [0.545 ,'Cl_in' , 'mM','original/ion_model'],
                'Na_in' : [29.98 , 'Na_in', 'mM','original/ion_model'],


                # NOTE: external concentration were normed, that the sum for c_e is approximatly 240mM
                #       faktor * 1126 ist für die Normierung da
                'H_out' : [(3.162e-3)* 1126 , 'H_out', 'mM','original/ion_model'],
                'K_out' : [0.1 * 1126, 'K_out', 'mM','original/ion_model'],
                'Cl_out' : [0.1 * 1126, 'Cl_out', 'mM','original/ion_model'],
                'Na_out' : [0.01 * 1126 , 'Na_out', 'mM','original/ion_model'],

                # NOTE: Sorbitol is now implemented as an ODE 
                'Sorbitol_out': [0, 'Sorbitol_out', 'mM'],

                # energy
                'ATP' : [2.477, 'ATP', 'mM'],
                #ATP = [1.3, 'ATP', 'mM']

                # membrane voltage
                'Deltaphi' : [-0.168, 'Deltaphi', 'V'],

                # changeable coefficients
                'L_ArH' : [0, 'L_ArH', '... s^-1'],
                'L_HH' : [1.62 * 1e-9, 'L_HH', '... s^-1'],

            #    c_i = [6.38904517734e-12, 'c_i', 'mmol', 'original/volume_model'] # internal concentration of osmolytes
                # NOTE: c_i is now calculated
                'c_i' : [0, 'c_i', 'mM', 'internal concentration of osmolytes']
                }

substance_for_c_i = ['H_in', 'K_in', 'Cl_in', 'Na_in', 'Glyc_in']

for i in substance_for_c_i:
    combined_models_init_values['c_i'][0] += combined_models_init_values[i][0]
