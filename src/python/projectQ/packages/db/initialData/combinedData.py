from projectQ.packages.values import SimulationTypes
from projectQ.packages.db.initialData.ModelData import ModelData, ParameterData as P, InitialValueData as I


combinedData = ModelData(
    type = SimulationTypes.combined,
    parameters = [
        P('T', 303.15, 'K'),
        P('R',  8.314, 'J K^-1 mol^-1'),
        P('F',  96485, 'C mol^-1'),

        P('k_phoPbs2',      39.22 /60, 's^-1'),
        P('k_dephoPbs2',    13.44 /60, 's^-1'),
        P('k_phoHog1', 11.2 * 1e3 /60, 'mM^-1 s^-1'),

        P('k_dephoHog1PPn',    4.144/60, 's^-1'),
        P('k_dephoHog1PPc',  0.09061/60, 's^-1'),
        P('k_impHog1PPc',      1.195/60, 's^-1'),
        P('k_s0Glyc',    5248 * 1e-3/60, 'mM s^-1'),
        P('k_s1Glyc',   56140 * 1e-3/60, 'mM s^-1'),
        P('k_s2Glyc',           1139/60, 's^-1'),
        P('k_tYt',          0.008934/60, 's^-1'),
        P('k_impHog1c',       0.7528/60, 's^-1'),
        P('k_expHog1PPn',      7.076/60, 's^-1'),
        P('k_exp0Glyc',        0.005/60, 's^-1'),
        P('k_s0Yt',  0.01211 * 1e-3 /60, 'mM s^-1'),
        P('k_exp1Glyc',     0.02963 /60, 's^-1'),
        P('k_s1Yt',           1.204 /60, 's^-1'),
        P('k_expHog1n',         6.36/60, 's^-1'),
        P('PI_t0',          0.875 * 1e6, 'Pa', 'turgor pressure/unstressed'),
        P('PI_i0',            1.5 * 1e6, 'Pa', 'internal osmotic pressure/unstressed'),
        P('PI_e0',          0.625 * 1e6, 'Pa', 'external osmotic pressure/unstressed'),
        P('Glyc_ex',                  0, 'mM', 'eine Konstante hier'),

        P('alpha', 0.18 * 1e6, 'Pa'),  # orginal: [0.398 * 1e6 ,'Pa']
        P('beta', 0.6, 'dimensionless'),
        P('gamma', 0.18 * 1e6, 'Pa'),  # original: [0.9626 *1e6 ,'Pa']
        P('tau' , 20 * 60 ,'s'),
        P('hill_exponent', 8, 'dimensionless'),
        P('hill_exponent_eflux', 12, 'dimensionless'),

        P('d' , 0.115,'um','cell wall thickness'),
        P('phi' , 1e-4,'Pa^{-1} s^{-1}', 'cell wall extensibility; fitted Altenburg 2018'),
        P('pi_c' , 2e5, 'Pa', 'critical turgor pressure'),
        P('Lp' , 1.19e-6, 'um s^{-1} Pa^{-1}', 'hydraulic conductivity'),
        P('nu' , 0.5, 'dimensionless', 'Poissons ratio'),
        P('k_uptake' , 2e-16, 'mmol s^{-1} um^{-2}'),
        P('k_consumption' , 2.5e-16, 'mmol s^{-1} um^{-3}'),
        P('E_3D' , 2.58e6, 'Pa', 'measured Youngs modulus; Goldenbogen & Giese et al. 2016'),
        P('E', 3440000.0, 'Pa'),

        # from ion model
        P('ATP_stimulus' , 2.5, 'mM'),

        # umgerechnetes Volumen für kombiniertes Hog Model
        P('V_out' , 2.85 * 1e12,'fL'),

        # neu definierte externe Umgebung--> Experiment naeher
        P('pbc' , 200,'mM pH^-1'),
        P('C_m' , 1e-2, 'xxxxxxx'),
        P('c_strich_ATP' , 0.316, 'mM'),
        P('K_eq' , 1e-6, 'dimensionless'),

        P('L_HHaG' , 0.0019  , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ArHaG' , -0.00195 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HNa' , -6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_NaH' , -6.31 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_KK' , 6.37 * 1e-11 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HCl' , 1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ClH' , 1.298 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_NaNa' , 3.03 * 1e-15 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_ClCl' , 1.04 * 1e-9 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_HK' , -2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'),
        P('L_KH' , -2.072097044 * 1e-16 , 'mol^2 J^-1 m^-2 s^-1'),

        P('k_incrHH' , 3.54 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'),
        P('k_incrArH' , -3.64 * 1e-9, 'mol^2 J^-1 m^-2 s^-2'),
        P('k_ATPincr' , 10, 'mol m^-3 s^-1'),
        # P('k_ATPdecr', 4.0, ''),
        P('k_ATPdecr', 'k_ATPincr / ATP_stimulus', ''),
        # P('k_decrArH', 1.8666666666666669e-06, ''),
        P('k_decrArH', 'k_incrArH / L_ArHaG', ''),
        # P('k_decrHH', 1.8631578947368422e-06, ''),
        P('k_decrHH', 'k_incrHH / L_HHaG', ''),
    ],
    initialValues = [
        # unphosphorylated Pbs2
        I('Pbs2', 4.24318676149895e-05, 'mM', 'original/hog_model'),
        # phosphorylated Pbs2
        I('Pbs2PP', 8.36732584742436e-05, 'mM', 'original/hog_model'),
        # unphosphorylated cytoplasmic Hog1
        I('Hog1c', 0.000207330463546301, 'mM', 'original/hog_model'),
        # phosphorylated cytoplasmic Hog1
        I('Hog1PPc', 0.000140156906030251, 'mM', 'original/hog_model'),
        # unphosphorylated nuclear Hog1
        I('Hog1n', 0.000246949330823297, 'mM', 'original/hog_model'),
        # phosphorylated nuclear Hog1
        I('Hog1PPn', 9.86274865600528e-05, 'mM', 'original/hog_model'),
        # intracellular glycerol
        I('Glyc_in', 67.7527785984978, 'mM', 'original/hog_model'),

        # Yt is the time delay for the expression of glycerol-producing proteins
        I('Yt', 0.00184722792271671, 'mM', 'original/hog_model'),

        # z = delay of transcriptional feedback on glycerol production
        I('z1', 1.21924446074792e-05, 'mM', 'original/hog_model'),
        I('z2', 3.96671525669479e-06, 'mM', 'original/hog_model'),
        I('z3', 3.40995283900317e-06, 'mM', 'original/hog_model'),
        I('z4', 3.38122235751438e-06, 'mM', 'original/hog_model'),

        I('r_os', 1.80312296228841, 'um', 'simulated/volume_model for V=58fl'),
        I('r_b', 0.602127912747231, 'um', 'simulated/volume_model for V=58fl'),
        I('r', 2.40525087503565, 'um', 'simulated/volume_model for V=58fl'),
        I('R_ref', 1.89092156373615, 'um', 'simulated/volume_model for V=58fl'),

        I('pi_t', 163938.005703829, 'Pa', 'turgor pressure; original/volume_model'),

        I('H_in', 0.439707918739414, 'mM', 'original/ion_model'),
        I('K_in', 0.287815305059543, 'mM', 'original/ion_model'),
        I('Cl_in', 309.843812761778, 'mM', 'original/ion_model'),
        I('Na_in', 30.5617653286767, 'mM', 'original/ion_model'),

        I('H_out', 3.24123794588396, 'mM'),
        I('K_out', 112.663403067036, 'mM'),
        I('Cl_out', 112.344284558393, 'mM'),
        I('Na_out', 11.2599982565733, 'mM'),

        I('Sorbitol_out', 0, 'mM'),

        # energy
        I('ATP', 1.27460975624028, 'mM'),

        # membrane voltage
        I('Deltaphi', 0.15583597951543, 'V'),

        # changeable coefficients
        I('L_ArH', 0, '... s^-1'),
        I('L_HH' , 1.62 * 1e-9, '... s^-1'),

        I('c_i', 304.356873706535, 'mM', 'internal concentration of osmolytes')
    ]
)

