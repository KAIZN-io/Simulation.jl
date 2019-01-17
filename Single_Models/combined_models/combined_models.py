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
                # 'w' : [ 4.688 * 1e-3 * 1e6,'J m^-3 mM^-1'],
                #'Lp' : [0.2497 / 60 * 1e-6 ,'um Pa^-1 s^-1'],
                # 'f_V_cyt' : [0.5 ,'dimensionless'],
                # 'n_Hog1_total' : [6780 ,'xxx', 'total number of Hog1'],
                # 'V_osPIt' : [30.63 ,'fL'],
                # 'V_os0' : [34.8 ,'fL', 'volume before osmotic change'],
                # 'V_b' : [ 23.2,'fL','fixed part of the cell volume'],
                # 'alpha': [0.398 * 1e6, 'Pa'],  # orginal: [0.398 * 1e6 ,'Pa']
                # 'beta' : [0.2992,'dimensionless'],  #original: [ 0.2992,'dimensionless']
                # 'gamma' : [0.9626 *1e6 ,'Pa'], #original: [0.9626 *1e6 ,'Pa']
                'alpha': [0.18 * 1e6, 'Pa'],  # orginal: [0.398 * 1e6 ,'Pa']  
                'beta': [0.6, 'dimensionless'],
                'gamma': [0.18 * 1e6, 'Pa'],  # original: [0.9626 *1e6 ,'Pa']
                'tau' : [20 * 60 ,'s'],
                # 'hill_exponent': [4, 'dimensionless'],
                # 'hill_exponent_eflux': [4, 'dimensionless'],
                'hill_exponent': [8, 'dimensionless'],
                'hill_exponent_eflux': [12, 'dimensionless'],

                # from volume model
                'd' : [0.115,'um','cell wall thickness'],
                'phi' : [1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility', 'fitted Altenburg 2018'],
                'pi_c' : [2e5, 'Pa', 'critical turgor pressure'],
                'Lp' : [1.19e-6, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'],
                'nu' : [0.5, 'dimensionless', 'Poissons ratio'],
                'k_uptake' : [2e-16, 'mmol s^{-1} um^{-2}'],
                'k_consumption' : [2.5e-16, 'mmol s^{-1} um^{-3}'],
                'E_3D' : [2.58e6, 'Pa', 'measured Youngs modulus', 'Goldenbogen & Giese et al. 2016'],
                'E': [3440000.0, 'Pa'],
                # from ion model
                'ATP_stimulus' : [2.5, 'mM'],

                #'V_out' : [2.85e-6,'m^3'],

                # umgerechnetes Volumen für kombiniertes Hog Model
                'V_out' : [2.85 * 1e12,'fL'],
                # neu definierte externe Umgebung--> Experiment naeher
                # 'V_out' : [28.95 * 1e3, 'fL'],

                'pbc' : [200,'mM pH^-1'],
                'C_m' : [1e-2, 'xxxxxxx'],
                'c_strich_ATP' : [0.316, 'mM'],
                'K_eq' : [1e-6, 'dimensionless'], 

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
                'k_ATPdecr': [4.0, ''],
                'k_decrArH': [1.8666666666666669e-06, ''],
                'k_decrHH': [1.8631578947368422e-06, ''],
                }

for key,value in combined_models_parameter.items():
    exec(key + '=value[0]')

modulus_adjustment = (1 - nu ** 2) ** (-1)  # dimensionless
E = modulus_adjustment * E_3D  # adjusted to 2D Young's modulus (surface)

k_ATPdecr = k_ATPincr / ATP_stimulus
k_decrArH =  k_incrArH / L_ArHaG
k_decrHH = k_incrHH / L_HHaG


combined_models_init_values = {
                # unphosphorylated Pbs2
                'Pbs2': [4.24318676149895e-05, 'Pbs2', 'mM', 'original/hog_model'],
                # phosphorylated Pbs2
                'Pbs2PP': [8.36732584742436e-05, 'Pbs2PP', 'mM', 'original/hog_model'],
                # unphosphorylated cytoplasmic Hog1
                'Hog1c': [0.000207330463546301, 'Hog1c', 'mM', 'original/hog_model'],
                # phosphorylated cytoplasmic Hog1
                'Hog1PPc': [0.000140156906030251, 'Hog1PPc', 'mM', 'original/hog_model'],
                # unphosphorylated nuclear Hog1
                'Hog1n': [0.000246949330823297, 'Hog1n', 'mM', 'original/hog_model'],
                # phosphorylated nuclear Hog1
                'Hog1PPn': [9.86274865600528e-05, 'Hog1PPn', 'mM', 'original/hog_model'],
                # intracellular glycerol
                'Glyc_in': [67.7527785984978, 'Glyc_in', 'mM', 'original/hog_model'],

                # Yt is the time delay for the expression of glycerol-producing proteins
                'Yt': [0.00184722792271671, 'Yt', 'mM', 'original/hog_model'],

                # z = delay of transcriptional feedback on glycerol production
                'z1': [1.21924446074792e-05, 'z1', 'mM', 'original/hog_model'],
                'z2': [3.96671525669479e-06, 'z2', 'mM', 'original/hog_model'],
                'z3': [3.40995283900317e-06, 'z3', 'mM', 'original/hog_model'],
                'z4': [3.38122235751438e-06, 'z4', 'mM', 'original/hog_model'],

                'r_os': [1.80312296228841, 'r_os', 'um', 'simulated/volume_model for V=58fl'],
                'r_b': [0.602127912747231, 'r_b', 'um', 'simulated/volume_model for V=58fl'],
                'r': [2.40525087503565, 'r', 'um', 'simulated/volume_model for V=58fl'],
                'R_ref': [1.89092156373615, 'R_ref', 'um', 'simulated/volume_model for V=58fl'],

                'pi_t': [163938.005703829, 'pi_t', 'Pa', 'turgor pressure', 'original/volume_model'],

                'H_in': [0.439707918739414, 'H_in', 'mM', 'original/ion_model'],
                'K_in': [0.287815305059543, 'K_in', 'mM', 'original/ion_model'],
                'Cl_in': [309.843812761778, 'Cl_in', 'mM', 'original/ion_model'],
                'Na_in': [30.5617653286767, 'Na_in', 'mM', 'original/ion_model'],

                'H_out': [3.24123794588396, 'H_out', 'mM'],
                'K_out': [112.663403067036, 'K_out', 'mM'],
                'Cl_out': [112.344284558393, 'Cl_out', 'mM'],
                'Na_out': [11.2599982565733, 'Na_out', 'mM'],

                'Sorbitol_out': [0, 'Sorbitol_out', 'mM'],

                # energy
                'ATP': [1.27460975624028, 'ATP', 'mM'],

                # membrane voltage
                'Deltaphi': [0.15583597951543, 'Deltaphi', 'V'],

                # changeable coefficients
                'L_ArH': [0, 'L_ArH', '... s^-1'],
                'L_HH' : [1.62 * 1e-9, 'L_HH', '... s^-1'],

                'c_i': [304.356873706535, 'c_i', 'mM', 'internal concentration of osmolytes']
                }

