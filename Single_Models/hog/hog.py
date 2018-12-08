hog_parameter = {
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

                'G' : [72.4607 ,'um^2'],
                'w' : [ 4.688 * 1e-3 * 1e6,'J m^-3 mM^-1'],
                'Lp' : [0.2497 / 60 * 1e-6 ,'um Pa^-1 s^-1'],
                'f_V_cyt' : [0.5 ,'dimensionless'],
                'n_Hog1_total' : [6780 ,'xxx', 'total number of Hog1'],
                'V_osPIt' : [30.63 ,'fL'],
                'V_os0' : [34.8 ,'fL', 'volume before osmotic change'],
                'V_b' : [ 23.2,'fL','fixed part of the cell volume'],
                'alpha' : [0.398 * 1e6 ,'Pa'],
                'beta' : [ 0.2992,'dimensionless'],
                'gamma' : [0.9626 *1e6 ,'Pa'],
                'tau' : [20 * 60 ,'s'],
                'n_0' : [4.176 * 1e3 ,'mmol'],
                'hill_exponent' : [8,'dimensionless'],
                'hill_exponent_eflux' : [12, 'dimensionless'],
                'max_NaCl' : [2 * 1e3, 'mM'],

                'T' : [303.15, 'K'],
                'R' : [8.314, 'J K^-1 mol^-1'],
                'F' : [96485, 'C mol^-1'],
                }

for key,value in hog_parameter.items():
    exec(key + '=value[0]')

hog_init_values = {

                'Pbs2' : [0.1231 * 1e-3, 'Pbs2', 'mM', 'original/hog_model'],              # unphosphorylated Pbs2
                'Pbs2PP' : [0.000616 * 1e-3, 'Pbs2PP', 'mM', 'original/hog_model'],            # phosphorylated Pbs2
                'Hog1c' : [0.3426 * 1e-3, 'Hog1c', 'mM', 'original/hog_model'],            # unphosphorylated cytoplasmic Hog1
                'Hog1PPc' : [0.004443 * 1e-3, 'Hog1PPc', 'mM', 'original/hog_model'],        # phosphorylated cytoplasmic Hog1
                'Hog1n' : [0.2918 * 1e-3, 'Hog1n', 'mM', 'original/hog_model'],              # unphosphorylated nuclear Hog1
                'Hog1PPn' : [0.00338 * 1e-3, 'Hog1PPn', 'mM', 'original/hog_model'],          # phosphorylated nuclear Hog1
                'Glyc_in' : [57600 * 1e-3, 'Glyc_in', 'mM', 'original/hog_model'],            # intracellular glycerol

                # Yt is the time delay for the expression of glycerol-producing proteins
                'Yt' : [1.811 * 1e-3, 'Yt', 'mM', 'original/hog_model'],
                'V_os' : [34.8, 'V_os', 'fL','original/hog_model'],

                'z1' : [0.00338 * 1e-3, 'z1', 'mM', 'original/hog_model'],              # z = delay of transcriptional feedback on glycerol production
                'z2' : [0.00338 * 1e-3, 'z2', 'mM', 'original/hog_model'],
                'z3' : [0.00338 * 1e-3, 'z3', 'mM', 'original/hog_model'],
                'z4' : [0.00338 * 1e-3, 'z4', 'mM', 'original/hog_model']
                }
